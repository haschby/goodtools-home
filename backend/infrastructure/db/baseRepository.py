from domain.ports.baseRepository import BaseRepositoryPort
from domain.models.baseModel import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import TypeVar, Optional, Type

MODEL = TypeVar('MODEL', bound=BaseModel)

class BaseRepository(BaseRepositoryPort[MODEL]):
    def __init__(
        self, 
        session: AsyncSession, 
        model: Type[BaseModel]
    ) -> None:
        self._session = session
        self._model = model
        
    async def count(self) -> int:
        command = select(func.count()).select_from(self._model)
        result = await self._session.execute(command)
        return result.scalar_one()
    
    async def create(self, models: list[MODEL]) -> Optional[list[MODEL]]:
        self._session.add_all(models)
        await self._session.commit()
        for item in models:
            await self._session.refresh(item)
        return models