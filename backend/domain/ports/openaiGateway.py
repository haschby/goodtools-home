from abc import ABC, abstractmethod

class OpenAIGateway(ABC):
    
    @abstractmethod
    async def chat_completion(self, message: str) -> dict:
        pass