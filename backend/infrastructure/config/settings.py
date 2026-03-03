from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    
    application_name: str
    application_version: str
    application_description: str
    application_author: str
    application_author_email: str
    
    grok_api_key: str = Field(..., env="GROK_API_KEY")
    grok_api_model: str = Field(..., env="GROK_API_MODEL")
    
    minio_host: str = Field(..., env="MINIO_HOST")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")
    minio_bucket: str = Field(..., env="MINIO_BUCKET")
    minio_region: str = Field(..., env="MINIO_REGION")
    
    redis_host: str = Field(..., env="REDIS_HOST")  
    redis_port: int = Field(..., env="REDIS_PORT")
    
    pennylane_api_token: str = Field(..., env="PENNYLANE_API_TOKEN")
    pennylane_api_public_url: str = Field(..., env="PENNYLANE_API_PUBLIC_URL")
    
    @property
    def database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
settings = Settings()