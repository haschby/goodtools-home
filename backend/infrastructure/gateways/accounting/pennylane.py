from application.ports.providers.accountingGateway import AccountingGateway
from domain.models.invoice import Invoice
from httpx import AsyncClient, Headers, HTTPStatusError, RequestError
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
        method: str = "GET",
        url: str = "/",
        params: dict | None = None,
        json: dict | None = None,
    ) -> dict | None:
        
        async with AsyncClient(
            base_url=self.api_url,
            headers=self.headers ) as client:
            
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )
                response.raise_for_status()
            except HTTPStatusError as e:
                print('@HTTPStatusError', e)
                # logger.error(
                #     "HTTP error %s on %s %s: %s",
                #     e.response.status_code, method, url, e.response.text,
                # )
                return None
            except RequestError as e:
                print('@RequestError', e)
                # logger.error("Request error on %s %s: %s", method, url, e)
                return None

        return response
        
    async def fetch_supplier_invoices(self, cursor: dict | None = None) -> dict | None:
        """
        Fetch supplier invoices from Pennylane.

        Query params:
          limit           : max results per page
          sort            : -date / -id
          filter          : JSON-encoded filter array
          payment_status  : eq, not_eq, in, not_in
        """
        filters = [
            {
                "field": "category_id",
                "operator": "in",
                "value": "28061807,28061805,28061789,28061787,28061765",
            },
            {
                "field": "payment_status",
                "operator": "eq",
                "value": "to_be_processed",
            },
            {
                "field": "id",
                "operator": "gt",
                "value": cursor["id"] if cursor else "0000000000",
            },
        ]
    
        result = await self.centralize_fetch(
            "GET",
            "/supplier_invoices",
            params={
            "limit": 100,
            "sort": "-id",
            "filter": json.dumps(filters) })
        
        if result:
            return result.json()
        else:
            return None
    
    async def fetch_supplier_info(self, supplier_ids: list[int]) -> dict | None:
        filters = [
            {
                "field": "id",
                "operator": "in",
                "value": ",".join(str(sid) for sid in supplier_ids),
            }
        ]
        result = await self.centralize_fetch(
            "GET",
            "/suppliers",
            params={
            "limit": 100,
            "filter": json.dumps(filters) })
        
        if result:
            return result.json()
        else:
            return None
    
    async def fetch_invoice_public_url(self, invoice_id: str) -> dict | None:
        result = await self.centralize_fetch(
            "GET",
            f"supplier_invoices/{invoice_id}")
        
        if result:
            return result.json()
        else:
            return None
        
    async def update_invoice_status(self, invoice_id: int, status: str) -> str | None:
        
        result = await self.centralize_fetch(
            "PUT",
            f"/supplier_invoices/{invoice_id}/payment_status",
            json={"payment_status": status} )
        
        if result:
            return result.text
        else:
            return None