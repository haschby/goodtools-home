from domain.ports.providers.accountingGateway import AccountingGateway
from domain.models.invoice import Invoice
from httpx import AsyncClient

class PennyLaneAccountingGateway(AccountingGateway[Invoice]):
    def __init__(self,
        api_url: str = settings.PENNYLANE_API_URL,
        api_token: str = settings.PENNYLANE_API_TOKEN
    ) -> None:
        self.api_url = api_url
        self.api_token = api_token