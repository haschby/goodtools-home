from domain.models.workflow import Workflow, Workflow_Step, StatusWorkflow
from .baseRepository import BaseRepository
from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Any

class WorkflowRepositoryImpl(BaseRepository[Workflow]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Workflow)
        
    async def get_by_id(self, id: str) -> Workflow:
        pass
    
    async def get_by_ref(self, ref: str) -> Workflow:
        result = await self._session.execute(
            select(Workflow)
            .options(selectinload(Workflow.steps))
            .where(
                or_(
                    Workflow.ref_pulling == ref,
                    Workflow.id == ref
                )
            )
        )
        return result.scalars().one_or_none()

    async def get_all(self) -> List[Any]:
        result = await self._session.execute(
            select(Workflow)
            .options(selectinload(Workflow.steps))
            .order_by(desc(Workflow.created_at), desc(Workflow.id))
        )
        return result.scalars().all()
    
    async def update_workflow_status(self,
        workflow_id: str,
        status: StatusWorkflow
    ) -> Workflow:
        workflow = await self.get_by_ref(workflow_id)
        workflow.status = status
        return await self.update_one(workflow)
    
    async def update_step_status(self,
        workflow_id: str,
        step_name: str,
        status: StatusWorkflow
    ) -> Workflow:
        workflow = await self.get_by_ref(workflow_id)
        step = next(s for s in workflow.steps if s.name == step_name)
        step.status = status
        return await self.update_one(step)