from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from src.models.core import CoreModel


class RunStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TriggerType(str, Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    API = "API"
    WEBHOOK = "WEBHOOK"


class TriggerRunRequest(CoreModel):
    run_config: Optional[Dict[str, Any]] = None
    environment: str = Field(
        default="development", pattern="^(development|staging|production)$"
    )
    triggered_by: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class PipelineRunCreate(CoreModel):
    pipeline_id: str
    trigger_type: TriggerType = TriggerType.MANUAL
    triggered_by: Optional[str] = None
    run_config: Optional[Dict[str, Any]] = None
    environment: str = "development"
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class PipelineRunResponse(CoreModel):
    id: str
    pipeline_id: str
    status: RunStatus
    trigger_type: TriggerType
    triggered_by: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    run_config: Optional[Dict[str, Any]] = None
    environment: str
    max_memory_usage: Optional[float] = None
    max_cpu_usage: Optional[float] = None
    success_count: int = 0
    failed_count: int = 0
    error_message: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class StageRunResponse(CoreModel):
    id: str
    pipeline_run_id: str
    stage_id: str
    status: RunStatus
    attempt_number: int = 1
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    logs: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class PipelineRunWithStages(PipelineRunResponse):
    stage_runs: List[StageRunResponse] = []
