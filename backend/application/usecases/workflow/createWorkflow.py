from application.ports.baseUsecase import BaseUsecase
from domain.models.workflow import Workflow
from application.ports.baseRepository import BaseRepositoryPort
from application.dtos.workflow import WorkflowCommand
from domain.models.workflow import StatusWorkflow, Workflow_Step

class CreateWorkflow(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository
    
    async def execute(self,
        command: WorkflowCommand
    ) -> list[Workflow] | Workflow:
        
        steps = [
            Workflow_Step(
                name=step.name,
                status=StatusWorkflow.PENDING,
                params={}
            )
            for step in command.steps
        ] if command.steps else []
        
        if hasattr(command, 'provider'):
            provider = command.provider
        else:
            provider = "internal"

        workflow = Workflow(
            ref_pulling=command.workflow_id,
            provider=provider,
            params=command.as_dict(),
            status=StatusWorkflow.PENDING,
            steps=steps
        )
        
        created_workflow = await self.repository.create([workflow])
        
        if len(created_workflow) > 1:
            return created_workflow
        
        return created_workflow[0]