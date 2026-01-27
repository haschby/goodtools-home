from pydantic import BaseModel


class S3Payload(BaseModel):
    bucket_name: str
    file_name: str
    text: str
    file_path: str