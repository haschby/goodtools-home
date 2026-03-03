from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.baseRepository import BaseRepositoryPort
from application.dtos.workflow import WorkflowCommand
from application.ports.baseUsecase import BaseUsecase
from domain.models.workflow import Workflow

class UpdateWorkflowSync(BaseActivity):
    def __init__(
        self,
        updateWorkflowUsecase: BaseUsecase
    ) -> None:
        self.updateWorkflowUsecase = updateWorkflowUsecase
    
    async def execute(self, workflow: Workflow) -> dict:
        return await self.updateWorkflowUsecase.execute(workflow)