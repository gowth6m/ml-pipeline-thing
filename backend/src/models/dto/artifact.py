from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, field_validator

from src.models.core import CoreModel


class ArtifactType(str, Enum):
    MODEL = "MODEL"
    DATASET = "DATASET"
    METRICS = "METRICS"
    PLOT = "PLOT"
    LOG = "LOG"
    CONFIG = "CONFIG"
    REPORT = "REPORT"
    OTHER = "OTHER"


class StorageType(str, Enum):
    LOCAL = "LOCAL"
    S3 = "S3"
    GCS = "GCS"
    AZURE = "AZURE"
    FTP = "FTP"


class ArtifactUpload(CoreModel):
    """DTO for uploading artifact metadata during pipeline creation (metadata only, no file storage)"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    artifact_type: ArtifactType
    file_content: str = Field(
        ...,
        description="Base64 encoded file content or reference (for metadata calculation only)",
    )
    file_name: str = Field(..., min_length=1, max_length=255)
    mime_type: Optional[str] = None
    storage_type: StorageType = StorageType.LOCAL
    storage_config: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    artifact_metadata: Optional[Dict[str, Any]] = None
    is_public: bool = False

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError("File name cannot be empty")
        return v


class ArtifactCreate(CoreModel):
    """DTO for creating artifacts via API"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    artifact_type: ArtifactType
    file_path: str = Field(..., min_length=1, max_length=1000)
    file_name: str = Field(..., min_length=1, max_length=255)
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    mime_type: Optional[str] = None
    storage_type: StorageType = StorageType.LOCAL
    storage_config: Optional[Dict[str, Any]] = None
    version: str = "1.0.0"
    tags: Optional[List[str]] = None
    artifact_metadata: Optional[Dict[str, Any]] = None
    is_public: bool = False


class ArtifactResponse(CoreModel):
    """DTO for artifact responses"""

    id: str
    name: str
    description: Optional[str] = None
    artifact_type: ArtifactType
    file_path: str
    file_name: str
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    mime_type: Optional[str] = None
    storage_type: StorageType
    storage_config: Optional[Dict[str, Any]] = None
    version: str
    stage_id: Optional[str] = None
    artifact_metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    is_active: bool
    is_public: bool
    download_count: int
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class DatasetCreate(CoreModel):
    """DTO for creating dataset metadata"""

    artifact_id: str
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    format: Optional[str] = None  # csv, json, parquet, etc.
    schema: Optional[Dict[str, Any]] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    missing_values_count: Optional[int] = None
    duplicate_rows_count: Optional[int] = None
    quality_score: Optional[float] = Field(None, ge=0, le=100)
    version: str = "1.0.0"
    source_datasets: Optional[List[str]] = None
    transformations: Optional[List[Dict[str, Any]]] = None
    dataset_metadata: Optional[Dict[str, Any]] = None


class DatasetResponse(CoreModel):
    """DTO for dataset responses"""

    id: str
    artifact_id: str
    name: str
    description: Optional[str] = None
    format: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    missing_values_count: Optional[int] = None
    duplicate_rows_count: Optional[int] = None
    quality_score: Optional[float] = None
    version: str
    source_datasets: Optional[List[str]] = None
    transformations: Optional[List[Dict[str, Any]]] = None
    dataset_metadata: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Include related artifact data
    artifact: Optional[ArtifactResponse] = None

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})


class ModelCreate(CoreModel):
    """DTO for creating model metadata"""

    artifact_id: str
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    model_type: Optional[str] = None  # classification, regression, clustering, etc.
    algorithm: Optional[str] = None  # random_forest, neural_network, etc.
    model_format: Optional[str] = None  # pickle, joblib, onnx, tensorflow, pytorch
    training_dataset_id: Optional[str] = None
    training_config: Optional[Dict[str, Any]] = None
    training_duration: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    validation_metrics: Optional[Dict[str, Any]] = None
    test_metrics: Optional[Dict[str, Any]] = None
    version: str = "1.0.0"
    parent_model_id: Optional[str] = None
    deployment_config: Optional[Dict[str, Any]] = None
    endpoint_url: Optional[str] = None
    framework: Optional[str] = None
    framework_version: Optional[str] = None
    python_version: Optional[str] = None
    dependencies: Optional[List[str]] = None
    model_metadata: Optional[Dict[str, Any]] = None


class ModelResponse(CoreModel):
    """DTO for model responses"""

    id: str
    artifact_id: str
    name: str
    description: Optional[str] = None
    model_type: Optional[str] = None
    algorithm: Optional[str] = None
    model_format: Optional[str] = None
    training_dataset_id: Optional[str] = None
    training_config: Optional[Dict[str, Any]] = None
    training_duration: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    validation_metrics: Optional[Dict[str, Any]] = None
    test_metrics: Optional[Dict[str, Any]] = None
    version: str
    parent_model_id: Optional[str] = None
    is_deployed: bool
    deployment_config: Optional[Dict[str, Any]] = None
    endpoint_url: Optional[str] = None
    framework: Optional[str] = None
    framework_version: Optional[str] = None
    python_version: Optional[str] = None
    dependencies: Optional[List[str]] = None
    model_metadata: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Include related artifact and dataset data
    artifact: Optional[ArtifactResponse] = None
    training_dataset: Optional[DatasetResponse] = None

    model_config = CoreModel.model_config.copy()
    model_config.update({"from_attributes": True})
