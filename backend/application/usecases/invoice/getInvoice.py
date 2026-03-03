import httpx
from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceCreateSchema
from application.ports.baseUsecase import BaseUsecase
from application.ports.providers.accountingGateway import AccountingGateway

class GetInvoice(BaseUsecase):
    def __init__(
        self,
        invoiceService: InvoiceService,
        accountingGateway: AccountingGateway
    ):
        self.invoiceService = invoiceService
        self.accountingGateway = accountingGateway
        
    async def execute(self, id: str) -> BaseResponseSchema:
        
        invoice = await self.invoiceService.get_by_id(id)
        if invoice is None:
            return BaseResponseSchema.response(
                message="Invoice not found",
                status_code=404,
                data=None
            )
        
        _data = InvoiceCreateSchema(**invoice.__dict__)
        
        public_url = await self.accountingGateway.fetch_invoice_public_url(_data.external_id)
        if public_url:
            file_url = public_url.get("public_file_url")
            _data.path = file_url
        
        return BaseResponseSchema.response(
            message="Invoice fetched" if invoice else "Invoice not fetched",
            status_code=201,
            data=_data
        )