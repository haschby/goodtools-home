from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceUpdateSchema
from domain.models.invoice import Invoice
from application.ports.invoiceRepository import InvoiceRepositoryPort
from application.ports.StorageGateway import StorageFileGateway
from application.ports.providers.accountingGateway import AccountingGateway
from typing import Optional

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
        existing_external_ids = [ invoice for invoice in existing_invoices ]
        invoices_to_create = [
            Invoice(**invoice.model_dump())
            for invoice in invoices
            if invoice.external_id not in existing_external_ids
        ]
        
        return await self.repository.create(invoices_to_create)
    
    async def get_by_id(self, id: str) -> Invoice:
        return await self.repository.get_by_id(id)
    
    
    async def get_all(self, status: Optional[str] = "All", cursor: Optional[dict] = None) -> list[Invoice]:
        invoices = await self.repository.get_all(status, cursor)
        return invoices
    
    # async def get_stats(self) -> StatsInvoices:
    #     return await self.invoiceRepository.get_stats()
    
    async def search(self, q: str, limit: int = 30, offset: int = 0) -> list[Invoice]:
        return await self.repository.search(q, limit, offset)
    
    
    async def update_invoice(self, invoice: InvoiceUpdateSchema) -> Invoice:
        existing_invoice = await self.get_by_id(invoice.id)
        if not existing_invoice:
            raise ValueError("Invoice not found")
        
        # update_invoice = invoice.model_dump(exclude_unset=True)
        
        for field, value in invoice.model_dump(exclude_unset=True).items():
            setattr(existing_invoice, field, value)
        
        return await self.repository.update(existing_invoice)