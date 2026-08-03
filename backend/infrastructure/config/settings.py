import os
from enum import Enum
from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PROD = "PROD"


class StorageProvider(str, Enum):
    MINIO = "MINIO"
    AWS = "AWS"


class Settings(BaseSettings):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('init settings', self.application_name)
    
    model_config = SettingsConfigDict(
        env_file='.env' if os.path.exists('.env') else None, 
        env_file_encoding='utf-8',
        extra='ignore'
    )

    environment: Environment = Field(Environment.LOCAL, env="ENVIRONMENT")
    
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    
    application_name: str = Field(..., env="APPLICATION_NAME")
    application_version: str = Field(..., env="APPLICATION_VERSION")
    application_description: str = Field(..., env="APPLICATION_DESCRIPTION")
    application_author: str = Field(..., env="APPLICATION_AUTHOR")
    application_author_email: str = Field(..., env="APPLICATION_AUTHOR_EMAIL")
    
    grok_api_key: str = Field(..., env="GROK_API_KEY")
    grok_api_model: str = Field(..., env="GROK_API_MODEL")
    
    minio_host: str = Field(..., env="MINIO_HOST")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")
    minio_bucket: str = Field(..., env="MINIO_BUCKET")
    minio_region: str = Field(..., env="MINIO_REGION")

    aws_access_key_id: str | None = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: str | None = Field(None, env="AWS_REGION")
    aws_s3_bucket: str | None = Field(None, env="AWS_S3_BUCKET")
    
    redis_host: str = Field(..., env="REDIS_HOST")  
    redis_port: int = Field(..., env="REDIS_PORT")
    
    pennylane_api_token: str = Field(..., env="PENNYLANE_API_TOKEN")
    pennylane_api_public_url: str = Field(..., env="PENNYLANE_API_PUBLIC_URL")
    
    goodcollect_base_url: str = Field(..., env="GOODCOLLECT_BASE_URL")
    
    gc_db_name: str = Field(..., env="GC_DB_NAME")
    gc_db_host: str = Field(..., env="GC_DB_HOST")
    gc_db_port: int = Field(..., env="GC_DB_PORT")
    gc_db_user: str = Field(..., env="GC_DB_USER")
    gc_db_pass: str = Field(..., env="GC_DB_PASS")

    @property
    def storage_provider(self) -> StorageProvider:
        return (
            StorageProvider.AWS
            if self.environment == Environment.PROD
            else StorageProvider.MINIO
        )

@dataclass
class DatabaseSchema:
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str
    
    def build_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

# settings = Settings()