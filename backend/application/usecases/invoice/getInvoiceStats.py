from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import StatsInvoicesResponseSchema

class GetInvoiceStats:
    def __init__(self, invoiceService: InvoiceService):
        self.invoiceService = invoiceService

    async def execute(self) -> BaseResponseSchema:
        stats = await self.invoiceService.get_stats()
        return BaseResponseSchema.response(
            message="Stats fetched" if stats else "Stats not fetched",
            status_code=201,
            data=stats
        )