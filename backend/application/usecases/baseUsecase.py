from abc import ABC, abstractmethod

class BaseUsecase(ABC):
    
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass