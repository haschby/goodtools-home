from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceResponseSchema

class CreateInvoice:
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, invoices: list[InvoiceCreateSchema]) -> list[InvoiceResponseSchema]:
        print('@INVOICES', invoices)
        invoices = await self.invoiceService.create_invoice(invoices)
        return BaseResponseSchema.response(
            message="Invoice created successfully" if invoices else "Invoice not created",
            status_code=201,
            data=[
                InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                for invoice in invoices
            ]
        )