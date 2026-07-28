from pydantic import BaseModel
from typing import (
    TypeVar, Any, Optional,
    List, Union, Generic, Dict,
    Any
)

T = TypeVar('T')
R = TypeVar('R', bound=BaseModel)

class BaseResponseSchema(BaseModel, Generic[T]):
    message: str
    status_code: int
    data: T | None = None
    
    class Config:
        from_attributes = True


class PaginatedResponseSchema(BaseModel, Generic[R]):
    items: List[R]
    page: int
    limit: int
    total: int
    total_pages: int
    total_by_status: Optional[dict] = None

    class Config:
        from_attributes = True