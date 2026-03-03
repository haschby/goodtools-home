from application.dtos.invoiceDto import InvoiceCreateSchema
from typing import List
from datetime import datetime, date
from domain.models.invoice import Invoice, EnumInvoiceStatus


def parse_date(date: str | None) -> date | None:
    if not date:
        return None
    
    # "invoice_date": "30/11/2025"
    # 31/10/2025
    date.replace('-', '/')
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date, fmt).date()
        except ValueError:
            pass
        
    return None

class InvoiceMapper:
    
    """{
  "amount": "178.84",
  "archived_at": null,
  "created_at": "2026-01-26T10:30:43.590752Z",
  "currency_amount_before_tax": "149.03",
  "currency_amount": "178.84",
  "currency_tax": "29.81",
  "currency": "EUR",
  "date": "2025-12-31",
  "deadline": "2025-12-31",
  "filename": "facture_304081252_r.v.d.l._01-25120103_31122025.pdf",
  "id": 4014099649,
  "invoice_number": "01-25120103",
  "label": "Facture R.V.D.L. - 01-25120103 (label généré)",
  "payment_status": "paid_offline",
  "remaining_amount_with_tax": "-178.84",
  "remaining_amount_without_tax": "-149.03",
  "tax": "29.81",
  "updated_at": "2026-01-26T14:47:34.819704Z",
  "reconciled": false,
  "public_file_url": "https://app.pennylane.com/public/invoice/pdf?encrypted_id=pqzeOaPj2itxWEzJfCG%2BFe1gMFO%2BHl1dtBGUGXPv9JWaVtmnJW8BefB90COAxulAkdiOorvJ1vzskpKuE3JF0%2FdvB9yFhOjaY85Wiu27ohBI9R49SxRJ6LhN--MT8hWwnNUTEs2PxX--3Ke39qWjV%2BfY%2FpvIWsHQNg%3D%3D",
  "exchange_rate": "1.0",
  "accounting_status": "validation_needed",
  "ledger_entry": {
    "id": 4014099649003
  },
  "transaction_reference": null,
  "supplier": {
    "id": 191196847,
    "url": "https://app.pennylane.com/api/external/v2/suppliers/191196847"
  },
  "invoice_lines": {
    "url": "https://app.pennylane.com/api/external/v2/supplier_invoices/4014099649/invoice_lines"
  },
  "categories": {
    "url": "https://app.pennylane.com/api/external/v2/supplier_invoices/4014099649/categories"
  },
  "payments": {
    "url": "https://app.pennylane.com/api/external/v2/supplier_invoices/4014099649/payments"
  },
  "matched_transactions": {
    "url": "https://app.pennylane.com/api/external/v2/supplier_invoices/4014099649/matched_transactions"
  },
  "external_reference": "GC-005849"
}
    """
    
    @staticmethod
    def from_pennylane(dto: dict) -> InvoiceCreateSchema:
        return InvoiceCreateSchema(
            name=dto.get("filename", None),
            path=dto.get("public_file_url", None),
            external_id=str(dto.get("id", None)),
            invoice_number=dto.get("invoice_number", None),
            invoice_date=parse_date(dto.get("date", None)),
            amount_ttc=dto.get("currency_amount", 0),
            amount_ht=dto.get("currency_amount_before_tax", 0),
            amount_tva=dto.get("currency_tax", 0),
            issuer_name=str(dto.get("supplier", {})) if dto.get("supplier", None) else None,
            construction_site_address=None,
            status=EnumInvoiceStatus.TBD,
            images=[],
            extracted_data=dto.get("extracted_data", {})
        )
    
    @staticmethod
    def from_pennylane_list(invoices: list[dict]) -> list[InvoiceCreateSchema]:
        return [
            InvoiceMapper.from_pennylane(invoice)
            for invoice in invoices
        ]
    
    @staticmethod
    def to_dto(invoice: any) -> InvoiceCreateSchema:
        chat_response = invoice.get("chat_response") or {}
        invoice_date = parse_date(invoice.get("invoice_date", None))

        invoice_data = InvoiceCreateSchema(
            amount_ttc=chat_response.get("amount_ttc", 0),
            amount_ht=chat_response.get("amount_ht", 0),
            amount_tva=chat_response.get("amount_tva", 0),
            issuer_name=chat_response.get("issuer_name"),
            construction_site_address=chat_response.get("construction_site_address", None),
            invoice_number=chat_response.get("invoice_number", None),
            invoice_date=invoice_date,

            name=invoice.get("path", None),
            gc_booking=invoice.get("gc_booking", None),
            status="A Traiter" if invoice.get("gc_booking", None) else "TBD",
            path=invoice.get("path", None),
            images=[],
            extracted_data=invoice.get("extracted_data", {}),
        )
        return invoice_data
    