from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.baseRepository import BaseRepositoryPort

class GetExternalInvoiceIdSync(BaseActivity):
    def __init__(self,
        search_invoice_usecase: BaseActivity
    ) -> None:
        self.search_invoice = search_invoice_usecase
        
    async def execute(self, invoice_id: str) -> str | None:
        invoice = await self.search_invoice.execute(
            q=invoice_id,
            limit=1,
            offset=0
        )
        
        if not invoice:
            return None
        
        return invoice[0].external_id