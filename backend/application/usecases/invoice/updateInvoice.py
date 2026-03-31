from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceUpdateSchema, InvoiceResponseSchema, InvoiceUpdateResponseSchema
from application.ports.baseUsecase import BaseUsecase

class UpdateInvoice(BaseUsecase):
    def __init__(
        self,
        invoiceService: InvoiceService,
        
        
    ):
        self.invoiceService = invoiceService

    async def execute(self, invoice: InvoiceUpdateSchema) -> InvoiceUpdateResponseSchema:
        invoice = await self.invoiceService.update_invoice(invoice)
        print('@UPDATED INVOICE IN USECASE', invoice)
        return InvoiceUpdateResponseSchema(
            message="Invoice updated" if invoice else "Invoice not updated",
            status_code=201,
            data=InvoiceUpdateSchema.model_validate(invoice, from_attributes=True)
        )