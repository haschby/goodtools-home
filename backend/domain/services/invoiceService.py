import sys
from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceUpdateSchema
from domain.models.invoice import Invoice
from application.ports.invoiceRepository import InvoiceRepositoryPort
from application.ports.StorageGateway import StorageFileGateway
from application.ports.providers.accountingGateway import AccountingGateway
from typing import Optional, Tuple, List

class InvoiceService:
    def __init__(self,
        invoiceRepository: InvoiceRepositoryPort,
        storage: StorageFileGateway
    ) -> None:
        self.repository = invoiceRepository
        self.storage = storage
        
    async def get_last_invoice_id(self) -> int | None:
        invoice = await self.repository.get_last_invoice_id()
        if invoice:
            return invoice
        return None
        
    async def create_invoice(self, invoices: list[InvoiceCreateSchema]) -> list[Invoice]:
        external_ids = [
            invoice.external_id
            for invoice in invoices
        ]
        
        existing_invoices = await self.repository.get_by_external_ids(external_ids)
        existing_external_ids = [ invoice.external_id for invoice in existing_invoices ]
        invoices_to_create = [
            Invoice(**invoice.model_dump())
            for invoice in invoices
            if invoice.external_id not in existing_external_ids
        ]
        
        return await self.repository.create(invoices_to_create)
    
    async def get_by_id(self, id: str) -> Invoice:
        return await self.repository.get_by_id(id)
    
    
    async def get_all(self,
        params: Optional[dict] = None
    ) -> Tuple[list[Invoice] | None, List[dict], int]:
    
        
        invoices, total_by_status_count = await self.repository.get_all(
            status=params['status'],
            page=params['page'],
            limit=params['limit'],
            query=params['query']
        )
        
        return invoices if invoices else None, total_by_status_count, await self.repository.count()
    
    # async def get_stats(self) -> StatsInvoices:
    #     return await self.invoiceRepository.get_stats()
    
    async def search(self, q: str, limit: int = 30, offset: int = 0) -> list[Invoice]:
        return await self.repository.search(q, limit, offset)
    
    
    async def update_invoice(self, invoices: List[InvoiceUpdateSchema]) -> List[Invoice]:
        
        invoice_ids = [ invoice.id for invoice in invoices ]
        existing_invoices = await self.repository.get_by_external_ids(invoice_ids)
        existing_map = { inv.id: inv for inv in existing_invoices }
        
        to_update = []
        for inv in invoices:
            existing_invoice = existing_map.get(inv.id)
            if not existing_invoice:
                continue
            
            for field, value in inv.model_dump(exclude_unset=True).items():
                setattr(existing_invoice, field, value)
            
            to_update.append(existing_invoice)
        
        updated_invoices = await self.repository.update(to_update)
        
        return updated_invoices