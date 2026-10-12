from domain.models.workflow import Workflow, Workflow_Step, StatusWorkflow
from .baseRepository import BaseRepository
from sqlalchemy import select, or_, desc, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Any, Optional, Tuple

class WorkflowRepositoryImpl(BaseRepository[Workflow]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Workflow)
        
    async def get_by_id(self, id: str) -> Workflow:
        pass
    
    async def get_by_ref(self, ref: str) -> Workflow:
        async with self._session() as session:
            result = await session.execute(
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
        async with self._session() as session:
            result = await session.execute(
                select(Workflow)
                .options(selectinload(Workflow.steps))
                .order_by(desc(Workflow.created_at), desc(Workflow.id))
            )
            return result.scalars().all()

    async def get_paginated(
        self,
        page: int = 1,
        limit: int = 30,
        query: Optional[str] = None,
        status: Optional[str] = "All"
    ) -> Tuple[List[Workflow], int]:
        """Return a page of workflows (most recent first) and the total number
        of workflows matching the filters (used to compute ``total_pages``)."""

        page = max(page or 1, 1)
        limit = max(limit or 30, 1)
        conditions = []

        if status and status != "All":
            try:
                conditions.append(Workflow.status == StatusWorkflow(status))
            except ValueError:
                pass

        if query:
            like = f"%{query.strip()}%"
            conditions.append(
                or_(
                    Workflow.id.ilike(like),
                    Workflow.ref_pulling.ilike(like),
                    Workflow.provider.ilike(like),
                    Workflow.message.ilike(like),
                    cast(Workflow.status, String).ilike(like),
                )
            )

        async with self._session() as session:
            items_stmt = (
                select(Workflow)
                .options(selectinload(Workflow.steps))
                .where(*conditions)
                .order_by(desc(Workflow.created_at), desc(Workflow.id))
                .limit(limit)
                .offset((page - 1) * limit)
            )
            count_stmt = select(func.count()).select_from(Workflow).where(*conditions)

            items = (await session.execute(items_stmt)).scalars().all()
            total = (await session.execute(count_stmt)).scalar_one()

        return items, total
    
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