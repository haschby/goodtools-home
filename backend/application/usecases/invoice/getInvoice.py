import httpx
from domain.services.invoiceService import InvoiceService
from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceDetailResponseSchema
from application.ports.baseUsecase import BaseUsecase
from application.ports.providers.accountingGateway import AccountingGateway
from application.ports.StorageGateway import StorageFileGateway
from domain.models.enums import EnumInvoiceType

class GetInvoice(BaseUsecase):
    def __init__(
        self,
        invoiceService: InvoiceService,
        accountingGateway: AccountingGateway,
        storage: StorageFileGateway
    ):
        self.invoiceService = invoiceService
        self.accountingGateway = accountingGateway
        self.storage = storage
        
    async def execute(self, id: str) -> InvoiceDetailResponseSchema:
        
        invoice = await self.invoiceService.get_by_id(id)
        if invoice is None:
            return InvoiceDetailResponseSchema(
                message="Invoice not found",
                status_code=404,
                data=None
            )
        
        _data = InvoiceCreateSchema(**invoice.__dict__)
        
        if _data.invoice_type == EnumInvoiceType.PROVIDER:
            pennylane_invoice = await self.accountingGateway.fetch_invoice_public_url(_data.external_id)
            print('@PUBLIC URL : ', pennylane_invoice);
            if pennylane_invoice:
                file_url = pennylane_invoice.get("public_file_url")
                _data.path = file_url
        else:
            file_url = await self.storage.presigned_url(_data.path)
            _data.path = file_url
            
        print('@DATA : ', _data);
        
        return InvoiceDetailResponseSchema(
            message="Invoice fetched" if invoice else "Invoice not fetched",
            status_code=201,
            data=_data
        )