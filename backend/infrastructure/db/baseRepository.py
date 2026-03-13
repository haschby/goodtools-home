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
        result = await self._session.execute(
            select(func.count()).select_from(self._model)
        )
        return result.scalar_one()
    
    async def create(self, models: list[MODEL]) -> list[MODEL]:
        self._session.add_all(models)
        await self._session.flush()
        for item in models:
            await self._session.refresh(item)
        return models
    
    async def update(self, models: list[MODEL]) -> list[MODEL]:
        merged = [await self._session.merge(model) for model in models]
        await self._session.flush()
        await self._session.commit()
        for item in merged:
            await self._session.refresh(item)
        return merged
    
    async def update_one(self, model: MODEL) -> MODEL:
        result = await self.update([model])
        return result[0]
            