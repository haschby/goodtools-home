from application.ports.baseRepository import BaseRepositoryPort
from domain.models.baseModel import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import TypeVar, Optional, Type

MODEL = TypeVar('MODEL', bound=BaseModel)

class BaseRepository(BaseRepositoryPort[MODEL]):
    def __init__(
        self, 
        session: AsyncSession,
        model: Type[BaseModel] ) -> None:
        self._session: AsyncSession = session
        self._model = model
        
    async def count(self) -> int:
        async with self._session as session:
            async with session.begin():
                command = select(func.count()).select_from(self._model)
                result = await session.execute(command)
            return result.scalar_one()
    
    async def create(self, models: list[MODEL]) -> Optional[list[MODEL]]:
        async with self._session as session:
            async with session.begin():
                session.add_all(models)
            
            for item in models:
                await session.refresh(item)
        return models
    
    async def update(self, models: list[MODEL]) -> Optional[list[MODEL]]:
        await self.create(models)
            