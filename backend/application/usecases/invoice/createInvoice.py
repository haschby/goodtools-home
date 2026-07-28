from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceDetailResponseSchema
from application.ports.baseUsecase import BaseUsecase

class CreateInvoice(BaseUsecase):
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, invoices: list[InvoiceCreateSchema]) -> InvoiceDetailResponseSchema:
        
        try:
            created_invoices = await self.invoiceService.create_invoice(invoices)
            return InvoiceDetailResponseSchema(
                message="Invoice created successfully" if invoices else "Invoice not created",
                status_code=201,
                data=[
                    InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                    for invoice in created_invoices
                ]
            )
        except Exception as e:
            return InvoiceDetailResponseSchema(
                message=f"Invoice not created {str(e)}",
                status_code=500,
                data=None
            )