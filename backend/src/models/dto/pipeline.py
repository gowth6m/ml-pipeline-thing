from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from src.models.core import CoreModel


class StageType(str, Enum):
    # Data Pipeline Stages
    DATA_INGESTION = "DATA_INGESTION"
    DATA_VALIDATION = "DATA_VALIDATION"
    DATA_PREPROCESSING = "DATA_PREPROCESSING"
    FEATURE_ENGINEERING = "FEATURE_ENGINEERING"
    DATA_SPLITTING = "DATA_SPLITTING"

    # Model Pipeline Stages
    MODEL_TRAINING = "MODEL_TRAINING"
    MODEL_VALIDATION = "MODEL_VALIDATION"
    MODEL_EVALUATION = "MODEL_EVALUATION"
    MODEL_TESTING = "MODEL_TESTING"

    # Deployment Pipeline Stages
    MODEL_REGISTRATION = "MODEL_REGISTRATION"
    MODEL_DEPLOYMENT = "MODEL_DEPLOYMENT"
    MODEL_MONITORING = "MODEL_MONITORING"

    # Analysis Stages
    EXPLORATORY_DATA_ANALYSIS = "EXPLORATORY_DATA_ANALYSIS"
    HYPERPARAMETER_TUNING = "HYPERPARAMETER_TUNING"
    MODEL_COMPARISON = "MODEL_COMPARISON"

    # Infrastructure Stages
    ENVIRONMENT_SETUP = "ENVIRONMENT_SETUP"
    RESOURCE_PROVISIONING = "RESOURCE_PROVISIONING"
    CLEANUP = "CLEANUP"

    # Custom Stages
    CUSTOM = "CUSTOM"


class StageStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class PipelineStageCreate(CoreModel):
    name: str = Field(..., min_length=1, max_length=255)
    stage_type: StageType
    custom_name: Optional[str] = Field(None, min_length=1, max_length=255)
    order: int = Field(..., ge=0)
    config: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None


class PipelineStageResponse(CoreModel):
    id: str
    name: str
    stage_type: StageType
    custom_name: Optional[str] = None
    status: StageStatus
    order: int
    config: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    output_path: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class PipelineCreate(CoreModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    stages: List[PipelineStageCreate] = Field(..., min_items=1)


class PipelineResponse(CoreModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    config: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class PipelineWithStages(PipelineResponse):
    stages: List[PipelineStageResponse] = []
