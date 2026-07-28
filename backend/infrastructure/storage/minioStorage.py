import uuid
import io
from datetime import timedelta
import requests

from dataclasses import dataclass
from application.ports.StorageGateway import StorageFileGateway
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
        file: "UploadFile | bytes",
        folder: str,
        file_name: str | None = None,
        content_type: str = "application/octet-stream",
    ) -> str:

        if isinstance(file, (bytes, bytearray)):
            file_byte = bytes(file)
        else:
            file_byte = await file.read()
            file_name = file_name or getattr(file, "filename", None)
            content_type = getattr(file, "content_type", None) or content_type

        object_name = f"{folder}/{uuid.uuid4()}_{file_name}"
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=io.BytesIO(file_byte),
            length=len(file_byte),
            content_type=content_type,
        )
        return object_name

    async def download_file(self, file_name: str) -> bytes:
        pass

    async def delete_file(self, file_name: str) -> bool:
        pass
    
    async def presigned_url(self, file_name: str, expires_in: int = 3600) -> str:
        return self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=file_name
        )