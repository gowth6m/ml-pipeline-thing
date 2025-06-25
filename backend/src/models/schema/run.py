import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.database.base import DatabaseModel
from src.models.schema.pipeline import PipelineStatus


class RunStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TriggerType(enum.Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    API = "API"
    WEBHOOK = "WEBHOOK"


class PipelineRun(DatabaseModel):
    __tablename__ = "pipeline_runs"

    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("pipelines.id"), nullable=False)

    # Run details
    status = Column(
        Enum(RunStatus), default=RunStatus.PENDING, nullable=False, index=True
    )
    trigger_type = Column(Enum(TriggerType), default=TriggerType.MANUAL, nullable=False)
    triggered_by = Column(String(255))  # User ID or system that triggered the run

    # Execution details
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Float)  # Total execution time in seconds

    # Configuration for this specific run
    run_config = Column(JSON)  # Run-specific configuration overrides
    environment = Column(
        String(50), default="development"
    )  # development, staging, production

    # Resource usage
    max_memory_usage = Column(Float)  # Peak memory usage in MB
    max_cpu_usage = Column(Float)  # Peak CPU usage percentage

    # Results
    success_count = Column(Integer, default=0)  # Number of successful stages
    failed_count = Column(Integer, default=0)  # Number of failed stages
    error_message = Column(Text)  # Error message if run failed
    output_data = Column(JSON)  # Final output data/results

    # Metadata
    tags = Column(JSON)  # List of tags for categorization
    notes = Column(Text)  # User notes about this run

    # Relationships
    pipeline = relationship("Pipeline", back_populates="runs")
    stage_runs = relationship(
        "StageRun", back_populates="pipeline_run", cascade="all, delete-orphan"
    )


class StageRun(DatabaseModel):
    __tablename__ = "stage_runs"

    pipeline_run_id = Column(
        UUID(as_uuid=True), ForeignKey("pipeline_runs.id"), nullable=False
    )
    stage_id = Column(
        UUID(as_uuid=True), ForeignKey("pipeline_stages.id"), nullable=False
    )

    # Run details
    status = Column(Enum(RunStatus), default=RunStatus.PENDING, nullable=False)
    attempt_number = Column(Integer, default=1)  # For retry functionality

    # Execution details
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Float)

    # Resource usage
    memory_usage = Column(Float)
    cpu_usage = Column(Float)

    # Output/Results
    output_data = Column(JSON)
    error_message = Column(Text)
    logs = Column(Text)  # Execution logs for this stage run

    # Relationships
    pipeline_run = relationship("PipelineRun", back_populates="stage_runs")
    stage = relationship("PipelineStage")
    artifacts = relationship(
        "Artifact", back_populates="stage_run", cascade="all, delete-orphan"
    )
