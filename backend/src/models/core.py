from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.core.database.base import Base, DatabaseModel


class CoreModel(BaseModel):
    """Base Pydantic model for core models"""

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        alias_generator=to_camel,
        populate_by_name=True,
    )


__all__ = ["Base", "DatabaseModel", "CoreModel"]
