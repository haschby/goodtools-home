from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

MODEL = TypeVar('MODEL_TYPE', bound=BaseModel)

class AccountingGateway(ABC, Generic[MODEL]):
    
    @abstractmethod
    async def get_by_id(self, model_id: str) -> MODEL:
        pass

    @abstractmethod
    async def update(self, model: MODEL) -> MODEL:
        pass