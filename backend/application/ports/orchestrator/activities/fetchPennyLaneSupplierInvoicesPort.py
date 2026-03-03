from application.ports.orchestrator.baseActivity import BaseActivity
from abc import abstractmethod

class FetchPennyLaneSupplierInvoicesPort(BaseActivity[dict, dict]):
    @abstractmethod
    async def execute(self, params: dict) -> dict:
        raise NotImplementedError