from pydantic import BaseModel
from typing import (
    TypeVar, Any, Optional,
    List, Union, Generic, Dict,
    Any
)

T = TypeVar('T', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)

class BaseResponseSchema(BaseModel, Generic[T]):
    message: str
    status_code: int
    data: Optional[T] = None
    
    class Config:
        from_attributes = True


class PaginatedResponseSchema(BaseModel, Generic[R]):
    items: List[R]
    page: int
    limit: int
    total: int
    total_pages: int

    class Config:
        from_attributes = True