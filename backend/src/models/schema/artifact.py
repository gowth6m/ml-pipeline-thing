import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.database.base import DatabaseModel


class ArtifactType(enum.Enum):
    """Types of artifacts that can be produced by pipeline stages"""

    MODEL = "MODEL"
    DATASET = "DATASET"
    METRICS = "METRICS"
    PLOT = "PLOT"
    LOG = "LOG"
    CONFIG = "CONFIG"
    REPORT = "REPORT"
    OTHER = "OTHER"


class StorageType(enum.Enum):
    """Storage backends for artifact files"""

    LOCAL = "LOCAL"
    S3 = "S3"
    GCS = "GCS"
    AZURE = "AZURE"


class ArtifactStatus(enum.Enum):
    """Status of artifact processing"""

    PENDING = "PENDING"
    READY = "READY"
    FAILED = "FAILED"


class Artifact(DatabaseModel):
    """
    Base artifact model representing a file or data object produced by a pipeline stage.
    """

    __tablename__ = "artifacts"

    # Basic identification
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    artifact_type = Column(Enum(ArtifactType), nullable=False, index=True)
    status = Column(
        Enum(ArtifactStatus), default=ArtifactStatus.PENDING, nullable=False
    )

    # File storage details
    file_path = Column(String(1000), nullable=False)  # Logical path to the artifact
    file_name = Column(String(255), nullable=False)  # Original filename
    file_size = Column(Integer)  # Size in bytes

    # Storage configuration
    storage_type = Column(Enum(StorageType), default=StorageType.S3, nullable=False)
    storage_config = Column(JSON)  # Storage-specific configuration

    # Pipeline relationships
    stage_id = Column(
        UUID(as_uuid=True), ForeignKey("pipeline_stages.id"), nullable=False
    )
    stage_run_id = Column(
        UUID(as_uuid=True), ForeignKey("stage_runs.id"), nullable=False
    )

    # Creation tracking
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Metadata
    artifact_metadata = Column(JSON)  # General metadata
    is_active = Column(Boolean, default=True)  # Soft delete

    # Relationships
    stage = relationship("PipelineStage", back_populates="artifacts")
    stage_run = relationship("StageRun", back_populates="artifacts")

    # Specialized artifact relationships (one-to-one)
    dataset = relationship(
        "Dataset",
        back_populates="artifact",
        uselist=False,
        cascade="all, delete-orphan",
    )
    model = relationship(
        "Model", back_populates="artifact", uselist=False, cascade="all, delete-orphan"
    )


class Dataset(DatabaseModel):
    """
    Specialized artifact representing a dataset file.
    """

    __tablename__ = "datasets"

    # Link to base artifact (inheritance)
    artifact_id = Column(
        UUID(as_uuid=True), ForeignKey("artifacts.id"), nullable=False, unique=True
    )

    # Dataset-specific properties
    format = Column(String(50), nullable=False)  # csv, json, parquet, etc.

    # Basic statistics
    row_count = Column(Integer)
    column_count = Column(Integer)

    # Schema information
    schema = Column(JSON)  # Column definitions, data types

    # Relationships
    artifact = relationship("Artifact", back_populates="dataset")
    trained_models = relationship("Model", back_populates="training_dataset")


class Model(DatabaseModel):
    """
    Specialized artifact representing a trained machine learning model.
    """

    __tablename__ = "models"

    # Link to base artifact (inheritance)
    artifact_id = Column(
        UUID(as_uuid=True), ForeignKey("artifacts.id"), nullable=False, unique=True
    )

    # Model architecture and type
    model_type = Column(
        String(100), nullable=False
    )  # classification, regression, clustering, etc.
    algorithm = Column(
        String(100), nullable=False
    )  # random_forest, neural_network, etc.
    framework = Column(
        String(100), nullable=False
    )  # scikit-learn, tensorflow, pytorch, etc.

    # Model format
    model_format = Column(String(50), nullable=False)  # pickle, joblib, onnx, etc.

    # Training information
    training_dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"))
    training_config = Column(JSON)  # Hyperparameters, training settings

    # Performance metrics
    metrics = Column(JSON)  # Training metrics (accuracy, precision, recall, f1, etc.)

    # Relationships
    artifact = relationship("Artifact", back_populates="model")
    training_dataset = relationship("Dataset", back_populates="trained_models")
