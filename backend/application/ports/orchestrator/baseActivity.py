from abc import ABC, abstractmethod
from typing import Generic, TypeVar

INPUT = TypeVar('INPUT_TYPE')
OUTPUT = TypeVar('OUTPUT_TYPE')

class BaseActivity(ABC, Generic[INPUT, OUTPUT]):    
    @abstractmethod
    async def execute(self, params: INPUT) -> OUTPUT:
        raise NotImplementedError