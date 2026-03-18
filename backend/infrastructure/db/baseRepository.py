from application.ports.baseRepository import BaseRepositoryPort
from domain.models.baseModel import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import TypeVar, Optional, Type, Callable

MODEL = TypeVar('MODEL', bound=BaseModel)

class BaseRepository(BaseRepositoryPort[MODEL]):
    def __init__(
        self, 
        session: Callable[[], AsyncSession],
        model: Type[BaseModel]
    ) -> None:
        self._session = session  # c'est la factory
        self._model = model
        
    async def count(self) -> int:
        async with self._session() as session:
            result = await session.execute(
                select(func.count()).select_from(self._model)
            )
            return result.scalar_one()
    
    async def create(self, models: list[MODEL]) -> list[MODEL]:
        async with self._session() as session:
            session.add_all(models)
            await session.commit()
            for item in models:
                await session.refresh(item)
            return models
    
    async def update(self, models: list[MODEL]) -> list[MODEL]:
        async with self._session() as session:
            merged = [await session.merge(model) for model in models]
            await session.flush()
            await session.commit()
            for item in merged:
                await session.refresh(item)
            return merged
    
    async def update_one(self, model: MODEL) -> MODEL:
        result = await self.update([model])
        return result[0]