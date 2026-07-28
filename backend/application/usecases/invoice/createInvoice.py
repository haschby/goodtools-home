from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import (
    InvoiceResponseSchema,
    InvoiceCreateSchema,
    InvoiceListDetailResponseSchema
)
from application.ports.baseUsecase import BaseUsecase

class CreateInvoice(BaseUsecase):
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, invoices: list[InvoiceCreateSchema]) -> InvoiceListDetailResponseSchema:
        try:
            print('@INVOICES IN CREATE INVOICE USECASE')
            created_invoices = await self.invoiceService.create_invoice(invoices)
            return InvoiceListDetailResponseSchema(
                message="Invoice created successfully" if invoices else "Invoice not created",
                status_code=201,
                data=[
                    InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                    for invoice in created_invoices
                ]
            )
        except Exception as e:
            print('@ERROR IN CREATE INVOICE USECASE', e)
            return InvoiceListDetailResponseSchema(
                message=f"Invoice not created {str(e)}",
                status_code=500,
                data=None
            )