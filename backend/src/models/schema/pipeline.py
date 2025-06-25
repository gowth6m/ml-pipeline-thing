import enum
from typing import List

from sqlalchemy import (
    JSON,
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
from src.models.schema.artifact import ArtifactType


class PipelineStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Pipeline(DatabaseModel):
    __tablename__ = "pipelines"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(
        Enum(PipelineStatus), default=PipelineStatus.PENDING, nullable=False, index=True
    )
    config = Column(JSON)

    # Execution details
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Float)

    # Resource usage
    memory_usage = Column(Float)  # MB
    cpu_usage = Column(Float)  # Percentage

    # Relationships
    stages = relationship(
        "PipelineStage", back_populates="pipeline", cascade="all, delete-orphan"
    )
    runs = relationship(
        "PipelineRun", back_populates="pipeline", cascade="all, delete-orphan"
    )


class StageType(enum.Enum):
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


class StageStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class PipelineStage(DatabaseModel):
    __tablename__ = "pipeline_stages"

    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("pipelines.id"), nullable=False)
    name = Column(String(255), nullable=False)
    stage_type = Column(Enum(StageType), nullable=False, index=True)
    custom_name = Column(String(255))  # Used when stage_type is CUSTOM
    status = Column(Enum(StageStatus), default=StageStatus.PENDING, nullable=False)
    order = Column(Integer, nullable=False)  # Execution order

    # Stage configuration
    config = Column(JSON)
    dependencies = Column(JSON)  # List of stage IDs this stage depends on

    # Execution details
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Float)

    # Output/Results
    output_path = Column(String(500))
    metrics = Column(JSON)  # Stage-specific metrics
    logs = Column(Text)

    # Relationships
    pipeline = relationship("Pipeline", back_populates="stages")
    artifacts = relationship(
        "Artifact", back_populates="stage", cascade="all, delete-orphan"
    )


def get_expected_artifact_types(stage_type: StageType) -> List[ArtifactType]:
    """
    Returns the expected artifact types that a stage typically produces.

    Args:
        stage_type: The type of pipeline stage

    Returns:
        List of ArtifactType enums that this stage typically produces
    """
    stage_artifact_mapping = {
        # Data Pipeline Stages
        StageType.DATA_INGESTION: [ArtifactType.DATASET, ArtifactType.LOG],
        StageType.DATA_VALIDATION: [
            ArtifactType.REPORT,
            ArtifactType.METRICS,
            ArtifactType.LOG,
        ],
        StageType.DATA_PREPROCESSING: [
            ArtifactType.DATASET,
            ArtifactType.CONFIG,
            ArtifactType.LOG,
        ],
        StageType.FEATURE_ENGINEERING: [
            ArtifactType.DATASET,
            ArtifactType.CONFIG,
            ArtifactType.METRICS,
        ],
        StageType.DATA_SPLITTING: [ArtifactType.DATASET, ArtifactType.CONFIG],
        # Model Pipeline Stages
        StageType.MODEL_TRAINING: [
            ArtifactType.MODEL,
            ArtifactType.METRICS,
            ArtifactType.LOG,
            ArtifactType.CONFIG,
        ],
        StageType.MODEL_VALIDATION: [
            ArtifactType.METRICS,
            ArtifactType.REPORT,
            ArtifactType.PLOT,
        ],
        StageType.MODEL_EVALUATION: [
            ArtifactType.METRICS,
            ArtifactType.REPORT,
            ArtifactType.PLOT,
        ],
        StageType.MODEL_TESTING: [
            ArtifactType.METRICS,
            ArtifactType.REPORT,
            ArtifactType.LOG,
        ],
        # Deployment Pipeline Stages
        StageType.MODEL_REGISTRATION: [
            ArtifactType.MODEL,
            ArtifactType.CONFIG,
            ArtifactType.REPORT,
        ],
        StageType.MODEL_DEPLOYMENT: [
            ArtifactType.CONFIG,
            ArtifactType.LOG,
            ArtifactType.METRICS,
        ],
        StageType.MODEL_MONITORING: [
            ArtifactType.METRICS,
            ArtifactType.REPORT,
            ArtifactType.LOG,
        ],
        # Analysis Stages
        StageType.EXPLORATORY_DATA_ANALYSIS: [
            ArtifactType.REPORT,
            ArtifactType.PLOT,
            ArtifactType.METRICS,
        ],
        StageType.HYPERPARAMETER_TUNING: [
            ArtifactType.MODEL,
            ArtifactType.METRICS,
            ArtifactType.CONFIG,
        ],
        StageType.MODEL_COMPARISON: [
            ArtifactType.REPORT,
            ArtifactType.METRICS,
            ArtifactType.PLOT,
        ],
        # Infrastructure Stages
        StageType.ENVIRONMENT_SETUP: [ArtifactType.CONFIG, ArtifactType.LOG],
        StageType.RESOURCE_PROVISIONING: [ArtifactType.CONFIG, ArtifactType.LOG],
        StageType.CLEANUP: [ArtifactType.LOG],
        # Custom Stages
        StageType.CUSTOM: [ArtifactType.LOG],
    }

    return stage_artifact_mapping.get(stage_type, [ArtifactType.LOG])
