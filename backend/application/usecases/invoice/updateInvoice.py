from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceUpdateSchema, InvoiceResponseSchema, InvoiceUpdateResponseSchema
from application.ports.baseUsecase import BaseUsecase
from typing import List


class UpdateInvoice(BaseUsecase):
    def __init__(
        self,
        invoiceService: InvoiceService
    ):
        self.invoiceService = invoiceService

    async def execute(self, invoices: List[InvoiceUpdateSchema]) -> List[InvoiceUpdateResponseSchema] | InvoiceUpdateResponseSchema:
        
        updated_invoices = await self.invoiceService.update_invoice(invoices)
        
        print('@UPDATED INVOICES : ', updated_invoices)
        
        if updated_invoices is None:
            return InvoiceUpdateResponseSchema(
                message="No invoices updated",
                status_code=404,
                data=None
            )
        
        if len(updated_invoices) > 1:
            return InvoiceUpdateResponseSchema(
                message="Invoices updated",
                status_code=201,
                data=[
                    InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                    for invoice in updated_invoices
                ]
            )
        
        return InvoiceUpdateResponseSchema(
            message="Invoice updated",
            status_code=201,
            data=InvoiceResponseSchema.model_validate(updated_invoices[0], from_attributes=True)
        )