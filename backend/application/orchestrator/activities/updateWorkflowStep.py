from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.baseRepository import BaseRepositoryPort

class UpdateWorkflowStep(BaseActivity):
    def __init__(self, workflow_repository: BaseRepositoryPort) -> None:
        self.workflow_repository = workflow_repository
    
    async def execute(self, params: dict) -> dict:
        return await self.workflow_repository.update_workflow_step(params)