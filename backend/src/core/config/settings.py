from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "ML Pipeline Thing API"
    app_description: str = "ML Pipeline Thing API"
    version: str = "0.1.0"
    debug: bool = False
    environment: str = Field(
        default="development",
        description="Environment: development, staging, production",
    )

    # Server settings
    host: str = "0.0.0.0"
    port: int = 9095
    workers: int = 1

    # Database settings
    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/ml_pipeline_thing"
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    use_migrations: bool = True

    # Redis/Cache settings
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600

    # ML Pipeline settings
    max_concurrent_pipelines: int = 5
    pipeline_timeout: int = 3600
    model_storage_path: str = "./models"
    data_storage_path: str = "./data"
    artifact_storage_path: str = "./artifacts"

    # Monitoring and Logging
    log_level: str = "INFO"
    enable_metrics: bool = True
    metrics_port: int = 9090

    # Security settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production", min_length=32
    )
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # API settings
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8080",
            "https://ml-pipeline-thing.gowtham.io",
        ]
    )

    @property
    def effective_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        if self.environment == "production":
            return ["https://ml-pipeline-thing.gowtham.io"]
        return self.cors_origins

    # External services
    mlflow_tracking_uri: Optional[str] = None
    s3_bucket: Optional[str] = None
    aws_region: str = "eu-west-2"

    # Resource limits
    max_memory_per_pipeline: str = "2G"
    max_cpu_per_pipeline: float = 2.0

    @validator("environment")
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError(
                "Environment must be one of: development, staging, production"
            )
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                "Log level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
