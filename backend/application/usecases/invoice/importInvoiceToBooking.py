import logging
from typing import Any, Optional

from application.dtos.invoiceDto import InvoiceDetailResponseSchema, InvoiceResponseSchema
from application.ports.baseUsecase import BaseUsecase
from application.ports.providers.accountingGateway import AccountingGateway
from domain.mappers.invoiceMapper import InvoiceMapper
from domain.models.enums import EnumInvoiceStatus, EnumInvoiceType
from domain.models.invoice import Invoice
from domain.services.invoiceService import InvoiceService

logger = logging.getLogger("Goodtools.Application")


class ImportInvoiceToBooking(BaseUsecase):
    """Import a supplier invoice from the accounting provider (Pennylane)
    and attach it to a GoodCollect booking as a new rentability line.

    Steps:
      1. Check the invoice is not already known locally.
      2. Fetch the supplier invoice from the accounting gateway.
      3. Map it and persist it in database, linked to the booking.

    After `execute`, `gc_sync_needed` tells the caller whether the GC
    rentability line must be synchronised (invoice created / linked).
    """

    def __init__(
        self,
        invoiceService: InvoiceService,
        accountingGateway: AccountingGateway,
    ) -> None:
        self.invoiceService = invoiceService
        self.accountingGateway = accountingGateway
        self.gc_sync_needed: bool = False
        self.invoice_id: Optional[str] = None

    async def execute(self, booking_id: int, external_id: str) -> InvoiceDetailResponseSchema:
        self.gc_sync_needed = False
        self.invoice_id = None

        external_id = (external_id or "").strip()
        if not external_id:
            return self._error("Invoice id is required", 400)

        gc_booking = str(booking_id)

        # 1. Already known locally ?
        try:
            existing = await self.invoiceService.repository.get_by_external_ids([external_id])
        except Exception as e:
            logger.exception("ImportInvoiceToBooking: failed to check existing invoice")
            return self._error(f"Failed to check existing invoice: {str(e)}", 500)

        existing = next((inv for inv in existing if inv.external_id == external_id), None)
        if existing is not None:
            return await self._handle_existing(existing, gc_booking)

        # 2. Fetch from the accounting provider
        try:
            remote = await self.accountingGateway.get_supplier_invoice(external_id)
        except Exception as e:
            logger.exception("ImportInvoiceToBooking: accounting gateway error")
            return self._error(f"Failed to fetch invoice from Pennylane: {str(e)}", 502)

        if not remote:
            return self._error(f"Invoice {external_id} not found in Pennylane", 404)

        if remote.get("archived_at"):
            return self._error(f"Invoice {external_id} is archived in Pennylane", 409)

        # 3. Map & persist
        try:
            remote["supplier"] = await self._resolve_supplier_name(remote.get("supplier"))

            invoice_data = InvoiceMapper.from_pennylane(remote)
            invoice_data.gc_booking = gc_booking
            invoice_data.invoice_type = EnumInvoiceType.PROVIDER
            invoice_data.status = EnumInvoiceStatus.TO_BE_TRAITED

            created = await self.invoiceService.repository.create(
                [Invoice(**invoice_data.model_dump())]
            )
        except Exception as e:
            logger.exception("ImportInvoiceToBooking: failed to create invoice")
            return self._error(f"Failed to create invoice: {str(e)}", 500)

        if not created:
            return self._error("Invoice not created", 500)

        invoice = created[0]
        self.invoice_id = invoice.id
        self.gc_sync_needed = True

        return InvoiceDetailResponseSchema(
            message="Invoice imported and linked to booking",
            status_code=201,
            data=InvoiceResponseSchema.model_validate(invoice, from_attributes=True),
        )

    async def _handle_existing(self, invoice: Invoice, gc_booking: str) -> InvoiceDetailResponseSchema:
        current_booking = getattr(invoice, "gc_booking", None)

        if current_booking == gc_booking:
            return self._error("Invoice already linked to this booking", 409)

        if current_booking:
            return self._error(
                f"Invoice already linked to booking #{current_booking}", 409
            )

        # Known invoice without booking: simply attach it.
        try:
            invoice.gc_booking = gc_booking
            if invoice.status in (None, EnumInvoiceStatus.TBD, EnumInvoiceStatus.TBD.value):
                invoice.status = EnumInvoiceStatus.TO_BE_TRAITED
            updated = await self.invoiceService.repository.update_one(invoice)
        except Exception as e:
            logger.exception("ImportInvoiceToBooking: failed to link existing invoice")
            return self._error(f"Failed to link invoice to booking: {str(e)}", 500)

        self.invoice_id = updated.id
        self.gc_sync_needed = True

        return InvoiceDetailResponseSchema(
            message="Cette facture est déjà liée à un autre booking",
            status_code=409,
            data=InvoiceResponseSchema.model_validate(updated, from_attributes=True),
        )

    async def _resolve_supplier_name(self, supplier: Any) -> Optional[str]:
        if not supplier:
            return None
        if isinstance(supplier, str):
            return supplier

        supplier_id = supplier.get("id") if isinstance(supplier, dict) else None
        if not supplier_id:
            return None

        response = await self.accountingGateway.fetch_supplier_info([supplier_id])
        items = response.get("items", []) if response else []
        mapping = {item["id"]: item.get("name") for item in items if item.get("id")}
        return mapping.get(supplier_id)

    @staticmethod
    def _error(message: str, status_code: int) -> InvoiceDetailResponseSchema:
        return InvoiceDetailResponseSchema(message=message, status_code=status_code, data=None)
