from application.ports.baseUsecase import BaseUsecase
from domain.models.workflow import Workflow
from application.ports.baseRepository import BaseRepositoryPort

class UpdateWorkflow(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository
    
    async def execute(self, workflow: list[Workflow] | Workflow) -> list[Workflow] | Workflow:
        workflows = workflow if isinstance(workflow, list) else [workflow]
        return await self.repository.update(workflows)