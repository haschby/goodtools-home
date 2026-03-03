from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.baseRepository import BaseRepositoryPort
from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowCommand

class CreateWorkflowSync(BaseActivity):
    def __init__(
        self,
        createWorkflowUsecase: BaseUsecase
    ) -> None:
        self.create_workflow = createWorkflowUsecase
    
    async def execute(self, command: WorkflowCommand) -> dict:
        return await self.create_workflow.execute(command)
    