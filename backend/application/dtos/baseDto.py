from pydantic import BaseModel
from typing import (
    TypeVar, Any, Optional,
    List, Union, Generic, Dict,
    Any
)

MODEL_TYPE = TypeVar('MODEL_TYPE', bound=BaseModel)

class BaseResponseSchema(BaseModel, Generic[MODEL_TYPE]):
    message: str
    status_code: int
    data: Optional[Union[List[MODEL_TYPE], MODEL_TYPE, Any]] = None
    
    @classmethod
    def response(
        cls, 
        message: str, 
        status_code: int, 
        data: Optional[Union[List[MODEL_TYPE], MODEL_TYPE, Any]] = None
    ):  
        
        print('=> BaseResponseSchema.response data : ', type(data))
        
        if data is None:
            data = None
        
        return {
            "message": message,
            "status_code": status_code,
            "data": data
        }

    class Config:
        from_attributes = True