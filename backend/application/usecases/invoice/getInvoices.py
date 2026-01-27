from dataclasses import dataclass
from domain.services.invoiceService import InvoiceService
from application.dtos.invoiceDto import InvoiceResponseSchema
from application.dtos.baseDto import BaseResponseSchema
from domain.ports.StorageGateway import StorageFileGateway
from typing import Optional

class GetInvoicesParams:
    status: Optional[str] = "All"
    cursor: Optional[dict] = None

class GetInvoices:
    def __init__(self,
        invoiceService: InvoiceService
    ) -> None:
        self.invoiceService = invoiceService
        
    async def execute(self, params: GetInvoicesParams) -> BaseResponseSchema:
        invoices = await self.invoiceService.get_all(params['status'], params['cursor'])
        return BaseResponseSchema.response(
            message="Invoices found" if invoices else "No invoices found",
            status_code=201,
            data=[ 
                InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                for invoice in invoices
            ] if invoices else None
        )