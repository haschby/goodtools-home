from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceUpdateSchema, InvoiceResponseSchema

class UpdateInvoice:
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, invoice: InvoiceUpdateSchema) -> InvoiceResponseSchema:
        invoice = await self.invoiceService.update_invoice(invoice)
        return BaseResponseSchema.response(
            message="Invoice updated" if invoice else "Invoice not updated",
            status_code=201,
            data=invoice
        )