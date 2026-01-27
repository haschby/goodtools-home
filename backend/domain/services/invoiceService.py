from application.dtos.invoiceDto import InvoiceCreateSchema, InvoiceUpdateSchema
from domain.models.invoice import Invoice
from domain.ports.invoiceRepository import InvoiceRepositoryPort
from domain.ports.StorageGateway import StorageFileGateway
from typing import Optional

class InvoiceService:
    def __init__(self,
        invoiceRepository: InvoiceRepositoryPort, 
        storage: StorageFileGateway
    ) -> None:
        self.repository = invoiceRepository
        self.storage = storage
        
    async def create_invoice(self, invoices: list[InvoiceCreateSchema]) -> list[Invoice]:
        return await self.repository.create(
            [
                Invoice(**invoice.model_dump())
                for invoice in invoices
            ]
        )
    
    async def get_by_id(self, id: str) -> Invoice:
        return await self.repository.get_by_id(id)
    
    async def update_invoice(self, invoice: InvoiceUpdateSchema) -> Invoice:
        existing_invoice = await self.get_by_id(invoice.id)
        if not existing_invoice:
            raise ValueError("Invoice not found")
        
        update_invoice = invoice.model_dump(exclude_unset=True)
        
        for key, value in update_invoice.items():
            setattr(existing_invoice, key, value)
        
        return await self.repository.update(existing_invoice)
    
    async def get_all(self, status: Optional[str] = "All", cursor: Optional[dict] = None) -> list[Invoice]:
        invoices = await self.repository.get_all(status, cursor)
        for invoice in invoices:
            invoice.images_url = await self.storage.presigned_url(invoice.path)
        return invoices
    
    # async def get_stats(self) -> StatsInvoices:
    #     return await self.invoiceRepository.get_stats()