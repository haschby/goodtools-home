from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceResponseSchema
from application.ports.baseUsecase import BaseUsecase

class SearchInvoice(BaseUsecase):
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self, q: str, limit: int = 30, offset: int = 0) -> list[InvoiceResponseSchema]:
        invoices = await self.invoiceService.search(q, limit, offset)
        print('@INVOICES', invoices)
        return BaseResponseSchema.response(
            message="Search query",
            status_code=201,
            data=[ 
                InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                for invoice in invoices
            ] if invoices else None
        )