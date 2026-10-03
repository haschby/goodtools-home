from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional

from application.dtos.invoiceDto import InvoiceResponseSchema, InvoiceDetailResponseSchema
from application.ports.baseUsecase import BaseUsecase
from application.ports.providers.accountingGateway import AccountingGateway
from domain.mappers.invoiceMapper import parse_date
from domain.services.invoiceService import InvoiceService


class RefreshInvoice(BaseUsecase):
    """Refresh a local invoice with the latest data from Pennylane.

    Fetches the supplier invoice from Pennylane (`get_supplier_invoice`),
    maps the remote fields onto the local invoice and only persists an
    update when at least one tracked field (issuer, amounts, tva, date,
    invoice number, ...) actually changed between the two sources.
    """

    # Local invoice attribute -> Pennylane payload key.
    FIELD_MAPPING = {
        "invoice_number": "invoice_number",
        "invoice_date": "date",
        "amount_ttc": "currency_amount",
        "amount_ht": "currency_amount_before_tax",
        "amount_tva": "currency_tax",
        "issuer_name": "supplier",
        "name": "filename",
        "path": "public_file_url",
    }

    def __init__(
        self,
        invoiceService: InvoiceService,
        accountingGateway: AccountingGateway,
    ) -> None:
        self.invoiceService = invoiceService
        self.accountingGateway = accountingGateway
        # Set after each `execute` so callers (routes) can decide whether a
        # downstream GC sync is needed. Mirrors UpdateInvoice.gc_booking_added_ids.
        self.changed_fields: List[str] = []
        self.gc_sync_needed: bool = False

    async def execute(self, id: str) -> InvoiceDetailResponseSchema:
        self.changed_fields = []
        self.gc_sync_needed = False

        invoice = await self.invoiceService.get_by_id(id)
        if invoice is None:
            return InvoiceDetailResponseSchema(
                message="Invoice not found",
                status_code=404,
                data=None,
            )

        if not invoice.external_id:
            return InvoiceDetailResponseSchema(
                message="Invoice has no external_id, nothing to refresh",
                status_code=400,
                data=None,
            )

        remote = await self.accountingGateway.get_supplier_invoice(invoice.external_id)
        if not remote:
            return InvoiceDetailResponseSchema(
                message="Failed to fetch supplier invoice from Pennylane",
                status_code=502,
                data=None,
            )

        # The raw payload exposes the supplier as {"id": ..., "url": ...}.
        # Resolve it to its name so we can match it against issuer_name.
        remote["supplier"] = await self._resolve_supplier_name(remote.get("supplier"))

        changed_fields = self._apply_changes(invoice, remote)

        if not changed_fields:
            return InvoiceDetailResponseSchema(
                message="Invoice already up to date",
                status_code=200,
                data=InvoiceResponseSchema.model_validate(invoice, from_attributes=True),
            )

        updated = await self.invoiceService.repository.update_one(invoice)

        self.changed_fields = changed_fields
        # The GC rentability line mirrors invoice.amount_ht, so it only needs
        # to be re-synced when the HT amount changed and the invoice is linked
        # to a GC booking.
        self.gc_sync_needed = "amount_ht" in changed_fields and bool(
            getattr(updated, "gc_booking", None)
        )

        return InvoiceDetailResponseSchema(
            message=f"Invoice refreshed ({', '.join(changed_fields)})",
            status_code=201,
            data=InvoiceResponseSchema.model_validate(updated, from_attributes=True),
        )

    async def _resolve_supplier_name(self, supplier: Any) -> Optional[str]:
        if not supplier:
            return None

        # Already a resolved name.
        if isinstance(supplier, str):
            return supplier

        supplier_id = supplier.get("id") if isinstance(supplier, dict) else None
        if not supplier_id:
            return None

        response = await self.accountingGateway.fetch_supplier_info([supplier_id])
        suppliers = response.get("items", []) if response else []
        mapping = {
            item["id"]: item.get("name")
            for item in suppliers
            if item.get("id")
        }
        return mapping.get(supplier_id)

    def _apply_changes(self, invoice: Any, remote: Dict[str, Any]) -> List[str]:
        changed_fields: List[str] = []

        for attr, remote_key in self.FIELD_MAPPING.items():
            raw_value = remote.get(remote_key)
            new_value = self._coerce(attr, raw_value)

            # Skip fields that Pennylane doesn't return, so we never wipe
            # existing local data with a null coming from a partial payload.
            if new_value is None:
                continue

            current_value = getattr(invoice, attr, None)
            if not self._is_equal(attr, current_value, new_value):
                setattr(invoice, attr, new_value)
                changed_fields.append(attr)

        return changed_fields

    @staticmethod
    def _coerce(attr: str, value: Any) -> Any:
        if value is None:
            return None

        if attr in ("amount_ttc", "amount_ht", "amount_tva"):
            try:
                return Decimal(str(value))
            except (InvalidOperation, ValueError, TypeError):
                return None

        if attr == "invoice_date":
            if isinstance(value, date):
                return value
            return parse_date(str(value))

        return str(value)

    @staticmethod
    def _is_equal(attr: str, current: Any, new: Any) -> bool:
        if attr in ("amount_ttc", "amount_ht", "amount_tva"):
            try:
                return Decimal(str(current)) == Decimal(str(new))
            except (InvalidOperation, ValueError, TypeError):
                return current == new

        return current == new
