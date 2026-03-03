from application.ports.baseUsecase import BaseUsecase
from domain.models.workflow import Workflow
from application.ports.baseRepository import BaseRepositoryPort

class GetWorkflow(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository
    
    async def execute(self, workflow_id: str) -> Workflow:
        return await self.repository.get_by_ref(workflow_id)