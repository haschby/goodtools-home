from abc import ABC, abstractmethod
from typing import BinaryIO
from application.dtos.gateway import UploadFile
    
class StorageFileGateway(ABC):
    @abstractmethod
    async def upload_file(
        self, 
        file: UploadFile | BinaryIO
    ) -> str:
        pass
    
    @abstractmethod
    async def download_file(
        self,
        file_name: str
    ) -> bytes:
        pass
    
    @abstractmethod
    async def presigned_url(
        self,
        file_name: str,
        expires_in: int = 3600
    ) -> str:
        pass
    
    @abstractmethod
    async def delete_file(
        self,
        file_name: str
    ) -> bool:
        pass