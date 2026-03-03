from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowStepCommand

class CreateWorkflowStepSync(BaseActivity):
    def __init__(
        self,
        create_workflow_step_usecase: BaseUsecase
    ) -> None:
        self.create_workflow_step_usecase = create_workflow_step_usecase
    
    async def execute(self, command: WorkflowStepCommand) -> dict:
        return await self.create_workflow_step_usecase.execute(
            command.workflow_id, command.step_name
        )