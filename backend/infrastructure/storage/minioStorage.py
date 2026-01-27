import uuid
import io
from datetime import timedelta

from dataclasses import dataclass
from domain.ports.StorageGateway import StorageFileGateway
from application.dtos.gateway import UploadFile
from minio import Minio


class MinioStorage(StorageFileGateway):
    def __init__(
        self,
        host: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
        secure: bool = False
    ) -> None:
        
        self.client = Minio(
            host,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            secure=secure,
        )
        self.bucket_name = bucket_name
    
    async def upload_file(
        self, 
        file: UploadFile
    ) -> tuple[any, bytes]:
        file_name = f"{str(uuid.uuid4())[:8]}.{file.filename}"
        file_byte = await file.read()
        
        file_id = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            data=io.BytesIO(file_byte),
            length=len(file_byte),
            content_type=file.content_type
        )
        return file_id, file_byte

    async def download_file(self, file_name: str) -> bytes:
        pass

    async def delete_file(self, file_name: str) -> bool:
        pass
    
    async def presigned_url(self, file_name: str, expires_in: int = 3600) -> str:
        return self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            expires=timedelta(seconds=expires_in)
        )