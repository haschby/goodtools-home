from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceResponseSchema

class GetInvoice:
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, id: str) -> BaseResponseSchema:
        invoice = await self.invoiceService.get_by_id(id)
        return BaseResponseSchema.response(
            message="Invoice fetched" if invoice else "Invoice not fetched",
            status_code=201,
            data=InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
        )