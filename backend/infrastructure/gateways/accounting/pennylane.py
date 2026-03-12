from application.ports.providers.accountingGateway import AccountingGateway
from domain.models.invoice import Invoice
from httpx import AsyncClient, Headers
import json

class PennyLaneAccountingGateway(AccountingGateway[Invoice]):
    def __init__(self,
        api_url: str,
        api_token: str
    ) -> None:
        self.api_url = api_url
        self.api_token = api_token
    
    @property
    def headers(self) -> Headers:
        return Headers({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        })
    
    async def centralize_fetch(
        self,
        url: str,
        params: dict,
        method: str = "GET"
    ) -> dict:
        
        async with AsyncClient(
            base_url=self.api_url,
            headers=self.headers ) as client:
            if (method == "GET"):
                response = await client.get(
                    url,
                    params=params
                )
            elif (method == "POST"):
                response = await client.post(
                    url,
                    json=params
                )
            return response.json()
        
    async def fetch_supplier_invoices(self, cursor: dict | None = None) -> Invoice:
        """
        Fetch supplier invoices from Pennylane
        /supplier_invoices:
        
        limit: 100
        filter: [{"field":"supplier_id","operator":"eq", "value":"191196847"}]
        sort: -date / -id
        payment_status: eq, not_eq, in, not_in (to_be_paid / paid / to_be_processed)
        id: lt, lteq, gt, gteq, eq, not_eq, in, not_in
        """
        filters = [
            {"field":"category_id","operator":"in", "value":"28061807,28061805,28061789,28061787,28061765"},
            {"field":"payment_status","operator":"eq","value":"to_be_processed"},
        ]
    
        return await self.centralize_fetch(f"/supplier_invoices", {
            "limit": 100,
            "sort": "-id",
            "filter": json.dumps(filters)
        })
    
    async def fetch_supplier_info(self, supplier_ids: list[int]) -> dict:
        filters = [
            { "field":"id","operator":"in", "value": f"{','.join([str(id) for id in supplier_ids])}" }
        ]
        return await self.centralize_fetch(f"/suppliers", {
            "limit": 100,
            "filter": json.dumps(filters)
        })
    
    async def fetch_invoice_public_url(self, invoice_id: str) -> str:
        filters = [
            { "field":"id","operator":"eq", "value": invoice_id }
        ]
        return await self.centralize_fetch(f"supplier_invoices/{invoice_id}", {
            "filter": json.dumps(filters)
        })
        
    async def update_invoice_status(self, invoice_id: str, status: str) -> dict:
        
        f'supplier_invoices/{invoice_id}/payment_status'
        payload = { "payment_status": status }
        
        await self.centralize_fetch(
            f'supplier_invoices/${invoice_id}/payment_status', {
            "body": json.dumps(payload)
        })