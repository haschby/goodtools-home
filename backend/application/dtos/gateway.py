from pydantic import BaseModel
from typing import Any, Protocol

class UploadFile(Protocol):
    filename: str
    content_type: str
    async def read(self) -> bytes: ...

class OpenAIResponse(BaseModel):
    content: Any
       