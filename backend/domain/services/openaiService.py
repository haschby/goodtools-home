from application.ports.openaiGateway import OpenAIGateway
from application.dtos.gateway import OpenAIResponse

class OpenAIService:
    def __init__(self, AIClientGateway: OpenAIGateway):
        self.AIClientGateway = AIClientGateway
        
    async def _chat_client_completion(self, text: str) -> OpenAIResponse:
        return await self.AIClientGateway.chat_completion(text)