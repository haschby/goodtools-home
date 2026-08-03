import uuid
import io

import boto3

from application.ports.StorageGateway import StorageFileGateway
from application.dtos.gateway import UploadFile


class S3Storage(StorageFileGateway):
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str
    ) -> None:
        
        self.client = boto3.client("s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            endpoint_url=f"https://s3.{region}.amazonaws.com",
        )
        self.bucket_name = bucket_name

    async def upload_file(
        self,
        file: "UploadFile | bytes",
        file_name: str | None = None,
        content_type: str = "application/octet-stream",
    ) -> str:

        if isinstance(file, (bytes, bytearray)):
            file_byte = bytes(file)
        else:
            file_byte = await file.read()
            file_name = file_name or getattr(file, "filename", None)
            content_type = getattr(file, "content_type", None) or content_type

        object_name = f"{uuid.uuid4()}_{file_name}"
        self.client.upload_fileobj(
            Fileobj=io.BytesIO(file_byte),
            Bucket=self.bucket_name,
            Key=object_name,
            ExtraArgs={"ContentType": content_type},
        )
        return object_name

    async def download_file(self, file_name: str) -> bytes:
        buffer = io.BytesIO()
        self.client.download_fileobj(
            Bucket=self.bucket_name,
            Key=file_name,
            Fileobj=buffer,
        )
        return buffer.getvalue()

    async def delete_file(self, file_name: str) -> bool:
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=file_name,
        )
        return True

    async def presigned_url(self, file_name: str, expires_in: int = 3600) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": file_name},
            ExpiresIn=expires_in,
        )
