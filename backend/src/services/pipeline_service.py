import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.exceptions import PipelineValidationError
from src.models.dto import (
    PaginationResponse,
    PipelineCreate,
    PipelineResponse,
    PipelineStageResponse,
    PipelineWithStages,
)
from src.models.schema.pipeline import (
    Pipeline,
    PipelineStage,
    PipelineStatus,
    StageStatus,
    StageType,
)

logger = logging.getLogger(__name__)


class PipelineService:
    def __init__(self, db: Session):
        self.db = db

    def create_pipeline(self, pipeline_data: PipelineCreate) -> PipelineWithStages:
        """Create a new pipeline with its stages"""
        try:
            self._validate_stage_dependencies(pipeline_data.stages)
            self._validate_custom_stages(pipeline_data.stages)

            db_pipeline = Pipeline(
                name=pipeline_data.name,
                description=pipeline_data.description,
                config=pipeline_data.config,
                status=PipelineStatus.PENDING,
            )

            self.db.add(db_pipeline)
            self.db.flush()

            for stage_data in pipeline_data.stages:
                db_stage = PipelineStage(
                    pipeline_id=db_pipeline.id,
                    name=stage_data.name,
                    stage_type=stage_data.stage_type,
                    custom_name=stage_data.custom_name,
                    order=stage_data.order,
                    config=stage_data.config,
                    dependencies=stage_data.dependencies,
                    status=StageStatus.PENDING,
                )
                self.db.add(db_stage)

            self.db.commit()
            self.db.refresh(db_pipeline)

            logger.info(f"Created pipeline {db_pipeline.id}: {db_pipeline.name}")
            return self._convert_to_response_with_stages(db_pipeline)

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create pipeline: {e}")
            raise

    def list_pipelines(self, skip: int = 0, limit: int = 100) -> List[PipelineResponse]:
        """List all pipelines"""
        pipelines = self.db.query(Pipeline).offset(skip).limit(limit).all()
        return [self._convert_to_response(p) for p in pipelines]

    def list_pipelines_paginated(
        self, page: int = 1, size: int = 100
    ) -> PaginationResponse[PipelineResponse]:
        """List pipelines with pagination"""
        skip = (page - 1) * size

        total = self.db.query(Pipeline).count()

        pipelines = self.db.query(Pipeline).offset(skip).limit(size).all()
        items = [self._convert_to_response(p) for p in pipelines]

        return PaginationResponse.create(
            items=items,
            total=total,
            page=page,
            size=size,
        )

    def get_pipeline(self, pipeline_id: str) -> Optional[PipelineResponse]:
        """Get a pipeline by ID"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            return None
        return self._convert_to_response(pipeline)

    def get_pipeline_with_stages(
        self, pipeline_id: str
    ) -> Optional[PipelineWithStages]:
        """Get a pipeline with all its stages"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            return None
        return self._convert_to_response_with_stages(pipeline)

    def delete_pipeline(self, pipeline_id: str) -> bool:
        """Delete a pipeline and all its data"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            return False

        try:
            self.db.delete(pipeline)
            self.db.commit()
            logger.info(f"Deleted pipeline {pipeline_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete pipeline {pipeline_id}: {e}")
            raise

    def _validate_stage_dependencies(self, stages):
        """Validate that stage dependencies are valid"""
        stage_orders = {stage.order for stage in stages}

        # Check for duplicate stage orders
        if len(stage_orders) != len(stages):
            raise PipelineValidationError(
                "Duplicate stage orders found. Each stage must have a unique order."
            )

        for stage in stages:
            if stage.dependencies:
                for dep_order in stage.dependencies:
                    try:
                        dep_order_int = int(dep_order)
                    except (ValueError, TypeError):
                        raise PipelineValidationError(
                            f"Stage {stage.name} has invalid dependency format: {dep_order}"
                        )

                    if dep_order_int not in stage_orders:
                        raise PipelineValidationError(
                            f"Stage {stage.name} depends on non-existent stage order {dep_order}"
                        )
                    if dep_order_int >= stage.order:
                        raise PipelineValidationError(
                            f"Stage {stage.name} cannot depend on later stage {dep_order}"
                        )

    def _validate_custom_stages(self, stages):
        """Validate that custom stages have a custom_name"""
        for stage in stages:
            if stage.stage_type == StageType.CUSTOM and not stage.custom_name:
                raise PipelineValidationError(
                    f"Stage {stage.name} with type CUSTOM must have a custom_name"
                )

    def _convert_to_response(self, pipeline: Pipeline) -> PipelineResponse:
        """Convert Pipeline model to response schema"""
        return PipelineResponse(
            id=str(pipeline.id),
            name=pipeline.name,
            description=pipeline.description,
            status=pipeline.status.value,
            config=pipeline.config,
            started_at=pipeline.started_at,
            completed_at=pipeline.completed_at,
            execution_time=pipeline.execution_time,
            memory_usage=pipeline.memory_usage,
            cpu_usage=pipeline.cpu_usage,
            created_at=pipeline.created_at,
            updated_at=pipeline.updated_at,
        )

    def _convert_to_response_with_stages(
        self, pipeline: Pipeline
    ) -> PipelineWithStages:
        """Convert Pipeline model to response schema with stages"""
        stage_responses = []
        for stage in pipeline.stages:
            stage_response = PipelineStageResponse(
                id=str(stage.id),
                name=stage.name,
                stage_type=stage.stage_type,
                custom_name=stage.custom_name,
                status=stage.status,
                order=stage.order,
                config=stage.config,
                dependencies=stage.dependencies,
                started_at=stage.started_at,
                completed_at=stage.completed_at,
                execution_time=stage.execution_time,
                output_path=stage.output_path,
                metrics=stage.metrics,
                created_at=stage.created_at,
                updated_at=stage.updated_at,
            )
            stage_responses.append(stage_response)

        stage_responses.sort(key=lambda x: x.order)

        return PipelineWithStages(
            id=str(pipeline.id),
            name=pipeline.name,
            description=pipeline.description,
            status=pipeline.status.value,
            config=pipeline.config,
            started_at=pipeline.started_at,
            completed_at=pipeline.completed_at,
            execution_time=pipeline.execution_time,
            memory_usage=pipeline.memory_usage,
            cpu_usage=pipeline.cpu_usage,
            created_at=pipeline.created_at,
            updated_at=pipeline.updated_at,
            stages=stage_responses,
        )
