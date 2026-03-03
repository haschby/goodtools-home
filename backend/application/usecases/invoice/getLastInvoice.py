from application.ports.baseUsecase import BaseUsecase
from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceResponseSchema

class GetLastInvoice(BaseUsecase):
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self) -> int | None:
        return await self.invoiceService.get_last_invoice_id()