from dataclasses import dataclass
from domain.services.invoiceService import InvoiceService
from application.dtos.invoiceDto import InvoiceResponseSchema, InvoiceListResponseSchema
from application.dtos.baseDto import BaseResponseSchema, PaginatedResponseSchema
from application.ports.StorageGateway import StorageFileGateway
from typing import Optional
from application.ports.baseUsecase import BaseUsecase
import math

class GetInvoicesParams:
    page: int
    limit: int
    status: Optional[str] = "All"
    query: Optional[str] = None

class GetInvoices(BaseUsecase):
    def __init__(self,
        invoiceService: InvoiceService
    ) -> None:
        self.invoiceService = invoiceService
        
    async def execute(self, params: GetInvoicesParams) -> InvoiceListResponseSchema:
        
        invoices, total_by_status_count, count = await self.invoiceService.get_all(params)
        
        items = []
        if invoices:
            items = [
                InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                for invoice in invoices
            ]
        
        total_by_status = { total["status"]: total['total'] for total in total_by_status_count }
        total_current_status = int(total_by_status.get(params.get('status', 'All'), 0))
            
        return InvoiceListResponseSchema(
            message="Invoices found" if items else "No invoices found",
            status_code=201,
            data=PaginatedResponseSchema(
                items=items,
                page=params.get('page', 1),
                limit=params.get('limit', 30),
                total_by_status=total_by_status,
                total_pages=math.ceil(total_current_status / params['limit']) if total_by_status else 1,
                total=count
            )
        )
    