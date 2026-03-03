from application.ports.baseUsecase import BaseUsecase
from application.ports.providers.accountingGateway import AccountingGateway
from application.ports.baseRepository import BaseRepositoryPort
from domain.models.workflow import Workflow
from domain.models.invoice import Invoice

class GetSupplierInvoices(BaseUsecase):
    def __init__(self,
        accounting_gateway: AccountingGateway
    ) -> None:
        self.accounting_gateway = accounting_gateway
    
    async def execute(self, workflow_id: str) -> None:
        invoices = await self.accounting_gateway.fetch_supplier_invoices()
        return invoices