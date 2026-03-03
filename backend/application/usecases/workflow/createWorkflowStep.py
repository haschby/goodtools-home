from application.ports.baseUsecase import BaseUsecase
from application.ports.baseRepository import BaseRepositoryPort
from domain.models.workflow import Workflow_Step

class CreateWorkflowStep(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository
    
    async def execute(self,
        workflow_id: str,
        step_name: str
    ) -> Workflow_Step:
        step = Workflow_Step(
            workflow_id=workflow_id,
            name=step_name,
            status=StatusWorkflow.PENDING
        )
        workflow = await self.repository.get_by_ref(workflow_id)
        workflow.steps.append(step)
        return await self.repository.update([workflow])