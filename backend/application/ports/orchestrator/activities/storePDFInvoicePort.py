from abc import abstractmethod
from application.dtos.workflow import WorkflowCommand
from application.ports.orchestrator.baseActivity import BaseActivity

class StorePDFInvoicePort(BaseActivity[WorkflowCommand, dict]):
    @abstractmethod
    async def execute(self, params: WorkflowCommand) -> dict:
        raise NotImplementedError