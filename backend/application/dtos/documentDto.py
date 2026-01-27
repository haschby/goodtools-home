from pydantic import BaseModel, field_serializer, model_validator
from uuid import UUID
from datetime import datetime
from typing import Optional


class DocumentCreateSchema(BaseModel):
    name: str
    path: str
    
    class Config:
        from_attributes = True
    
class DocumentResponseSchema(BaseModel):
    id: str
    name: str
    path: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
        
    class Config:
        from_attributes = True
        

class DocumentGetIdSchema(BaseModel):
    id: str