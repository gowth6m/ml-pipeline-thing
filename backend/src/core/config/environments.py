from typing import Any, Dict

from .settings import Settings


class DevelopmentSettings(Settings):
    debug: bool = True
    log_level: str = "DEBUG"
    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/ml_pipeline_thing_dev"
    )
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env.development"


class StagingSettings(Settings):
    debug: bool = False
    log_level: str = "INFO"
    database_url: str = (
        "postgresql://postgres:postgres@staging-db:5432/ml_pipeline_thing_staging"
    )
    redis_url: str = "redis://staging-redis:6379/0"
    max_concurrent_pipelines: int = 10

    class Config:
        env_file = ".env.staging"


class ProductionSettings(Settings):
    debug: bool = False
    log_level: str = "WARNING"
    workers: int = 4
    max_concurrent_pipelines: int = 20
    database_pool_size: int = 20
    database_max_overflow: int = 50
    cors_origins: list = []  # Configure based on your production frontend domains

    class Config:
        env_file = ".env.production"


def get_settings(environment: str = "development") -> Settings:
    """
    Factory function to get settings based on environment.
    """
    settings_map: Dict[str, Any] = {
        "development": DevelopmentSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
    }

    settings_class = settings_map.get(environment, DevelopmentSettings)
    return settings_class()
