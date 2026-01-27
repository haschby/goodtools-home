from application.dtos.invoiceDto import InvoiceCreateSchema
from typing import List
from datetime import datetime, date


def parse_date(date: str | None) -> date | None:
    if not date:
        return None
    
    # "invoice_date": "30/11/2025"
    # 31/10/2025
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date, fmt).date()
        except ValueError:
            pass
        
    return None

class InvoiceMapper:
    
    @staticmethod
    def to_dto(invoice: any) -> InvoiceCreateSchema:
        print('@INVOICE', invoice)
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
        
        print('@INVOICE DATA', invoice_data)

        return invoice_data
    