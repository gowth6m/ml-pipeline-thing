"""Initial migration

Revision ID: 8354490d267e
Revises:
Create Date: 2025-06-27 13:27:04.610756

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8354490d267e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pipelines",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                name="pipelinestatus",
            ),
            nullable=False,
        ),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.Column("memory_usage", sa.Float(), nullable=True),
        sa.Column("cpu_usage", sa.Float(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pipelines_id"), "pipelines", ["id"], unique=False)
    op.create_index(op.f("ix_pipelines_name"), "pipelines", ["name"], unique=False)
    op.create_index(op.f("ix_pipelines_status"), "pipelines", ["status"], unique=False)
    op.create_table(
        "pipeline_runs",
        sa.Column("pipeline_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                name="runstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "trigger_type",
            sa.Enum("MANUAL", "SCHEDULED", "API", "WEBHOOK", name="triggertype"),
            nullable=False,
        ),
        sa.Column("triggered_by", sa.String(length=255), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.Column("run_config", sa.JSON(), nullable=True),
        sa.Column("environment", sa.String(length=50), nullable=True),
        sa.Column("max_memory_usage", sa.Float(), nullable=True),
        sa.Column("max_cpu_usage", sa.Float(), nullable=True),
        sa.Column("success_count", sa.Integer(), nullable=True),
        sa.Column("failed_count", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipelines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pipeline_runs_id"), "pipeline_runs", ["id"], unique=False)
    op.create_index(
        op.f("ix_pipeline_runs_status"), "pipeline_runs", ["status"], unique=False
    )
    op.create_table(
        "pipeline_stages",
        sa.Column("pipeline_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "stage_type",
            sa.Enum(
                "DATA_INGESTION",
                "DATA_VALIDATION",
                "DATA_PREPROCESSING",
                "FEATURE_ENGINEERING",
                "DATA_SPLITTING",
                "MODEL_TRAINING",
                "MODEL_VALIDATION",
                "MODEL_EVALUATION",
                "MODEL_TESTING",
                "MODEL_REGISTRATION",
                "MODEL_DEPLOYMENT",
                "MODEL_MONITORING",
                "EXPLORATORY_DATA_ANALYSIS",
                "HYPERPARAMETER_TUNING",
                "MODEL_COMPARISON",
                "ENVIRONMENT_SETUP",
                "RESOURCE_PROVISIONING",
                "CLEANUP",
                "CUSTOM",
                name="stagetype",
            ),
            nullable=False,
        ),
        sa.Column("custom_name", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "SKIPPED",
                name="stagestatus",
            ),
            nullable=False,
        ),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("dependencies", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.Column("output_path", sa.String(length=500), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("logs", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipelines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_pipeline_stages_id"), "pipeline_stages", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_pipeline_stages_stage_type"),
        "pipeline_stages",
        ["stage_type"],
        unique=False,
    )
    op.create_table(
        "stage_runs",
        sa.Column("pipeline_run_id", sa.UUID(), nullable=False),
        sa.Column("stage_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                name="runstatus",
            ),
            nullable=False,
        ),
        sa.Column("attempt_number", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.Column("memory_usage", sa.Float(), nullable=True),
        sa.Column("cpu_usage", sa.Float(), nullable=True),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("logs", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_run_id"],
            ["pipeline_runs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stage_id"],
            ["pipeline_stages.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stage_runs_id"), "stage_runs", ["id"], unique=False)
    op.create_table(
        "artifacts",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "artifact_type",
            sa.Enum(
                "MODEL",
                "DATASET",
                "METRICS",
                "PLOT",
                "LOG",
                "CONFIG",
                "REPORT",
                "OTHER",
                name="artifacttype",
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("PENDING", "READY", "FAILED", name="artifactstatus"),
            nullable=False,
        ),
        sa.Column("file_path", sa.String(length=1000), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column(
            "storage_type",
            sa.Enum("LOCAL", "S3", "GCS", "AZURE", name="storagetype"),
            nullable=False,
        ),
        sa.Column("storage_config", sa.JSON(), nullable=True),
        sa.Column("stage_id", sa.UUID(), nullable=False),
        sa.Column("stage_run_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("artifact_metadata", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["stage_id"],
            ["pipeline_stages.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stage_run_id"],
            ["stage_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_artifacts_artifact_type"), "artifacts", ["artifact_type"], unique=False
    )
    op.create_index(op.f("ix_artifacts_id"), "artifacts", ["id"], unique=False)
    op.create_index(op.f("ix_artifacts_name"), "artifacts", ["name"], unique=False)
    op.create_table(
        "datasets",
        sa.Column("artifact_id", sa.UUID(), nullable=False),
        sa.Column("format", sa.String(length=50), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=True),
        sa.Column("column_count", sa.Integer(), nullable=True),
        sa.Column("schema", sa.JSON(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifacts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("artifact_id"),
    )
    op.create_index(op.f("ix_datasets_id"), "datasets", ["id"], unique=False)
    op.create_table(
        "models",
        sa.Column("artifact_id", sa.UUID(), nullable=False),
        sa.Column("model_type", sa.String(length=100), nullable=False),
        sa.Column("algorithm", sa.String(length=100), nullable=False),
        sa.Column("framework", sa.String(length=100), nullable=False),
        sa.Column("model_format", sa.String(length=50), nullable=False),
        sa.Column("training_dataset_id", sa.UUID(), nullable=True),
        sa.Column("training_config", sa.JSON(), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifacts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["training_dataset_id"],
            ["datasets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("artifact_id"),
    )
    op.create_index(op.f("ix_models_id"), "models", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_models_id"), table_name="models")
    op.drop_table("models")
    op.drop_index(op.f("ix_datasets_id"), table_name="datasets")
    op.drop_table("datasets")
    op.drop_index(op.f("ix_artifacts_name"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_id"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_artifact_type"), table_name="artifacts")
    op.drop_table("artifacts")
    op.drop_index(op.f("ix_stage_runs_id"), table_name="stage_runs")
    op.drop_table("stage_runs")
    op.drop_index(op.f("ix_pipeline_stages_stage_type"), table_name="pipeline_stages")
    op.drop_index(op.f("ix_pipeline_stages_id"), table_name="pipeline_stages")
    op.drop_table("pipeline_stages")
    op.drop_index(op.f("ix_pipeline_runs_status"), table_name="pipeline_runs")
    op.drop_index(op.f("ix_pipeline_runs_id"), table_name="pipeline_runs")
    op.drop_table("pipeline_runs")
    op.drop_index(op.f("ix_pipelines_status"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_name"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_id"), table_name="pipelines")
    op.drop_table("pipelines")
    # ### end Alembic commands ###
