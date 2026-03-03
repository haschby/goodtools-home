from application.ports.baseUsecase import BaseUsecase
from domain.models.workflow import Workflow
from application.ports.baseRepository import BaseRepositoryPort
from typing import List

class GetWorkflows(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository
    
    async def execute(self) -> List[Workflow]:
        return await self.repository.get_all()