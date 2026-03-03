from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy import select, func

MODEL = TypeVar('MODEL_TYPE', bound=BaseModel)

class BaseRepositoryPort(ABC, Generic[MODEL]):
    
    @abstractmethod
    async def get_all(self) -> List[MODEL]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> MODEL:
        pass
    
    @abstractmethod
    async def create(self, model: MODEL) -> MODEL:
        pass