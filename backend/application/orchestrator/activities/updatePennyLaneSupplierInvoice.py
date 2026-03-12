from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.providers.accountingGateway import AccountingGateway

class UpdatePennyLaneSupplierInvoice(BaseActivity):
    def __init__(self,
        accounting_gateway: AccountingGateway
    ) -> None:
        self.pennylane_gateway = accounting_gateway
        
    async def execute(self, invoice_id: str) -> bool | None:
        if not invoice_id:
            return False
        
        try:
            await self.pennylane_gateway.update_invoice_status(invoice_id, "to_be_paid")
        except Exception as e:
            print('@ERROR', e)
            return None