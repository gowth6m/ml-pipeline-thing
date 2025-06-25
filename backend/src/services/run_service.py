import asyncio
import logging
import random
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.exceptions import PipelineNotFoundError, PipelineRunNotFoundError
from src.models.dto import (
    PaginationResponse,
    PipelineRunResponse,
    PipelineRunWithStages,
    StageRunResponse,
    TriggerRunRequest,
)
from src.models.schema.pipeline import (
    Pipeline,
    PipelineStage,
    get_expected_artifact_types,
)
from src.models.schema.run import PipelineRun, RunStatus, StageRun, TriggerType

logger = logging.getLogger(__name__)


class RunService:
    def __init__(self, db: Session):
        self.db = db

    def trigger_run(
        self, pipeline_id: str, trigger_data: TriggerRunRequest
    ) -> PipelineRunResponse:
        """Trigger a new pipeline run"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            raise PipelineNotFoundError(pipeline_id)

        try:
            db_run = PipelineRun(
                pipeline_id=pipeline_id,
                trigger_type=TriggerType.MANUAL,
                triggered_by=trigger_data.triggered_by,
                run_config=trigger_data.run_config,
                environment=trigger_data.environment,
                tags=trigger_data.tags,
                notes=trigger_data.notes,
                status=RunStatus.PENDING,
            )

            self.db.add(db_run)
            self.db.flush()

            stages = (
                self.db.query(PipelineStage)
                .filter(PipelineStage.pipeline_id == pipeline_id)
                .all()
            )

            for stage in stages:
                stage_run = StageRun(
                    pipeline_run_id=db_run.id,
                    stage_id=stage.id,
                    status=RunStatus.PENDING,
                )
                self.db.add(stage_run)

            self.db.commit()
            self.db.refresh(db_run)

            logger.info(f"Triggered run {db_run.id} for pipeline {pipeline_id}")

            asyncio.create_task(self._simulate_execution(db_run.id))

            return self._convert_to_response(db_run)

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to trigger run for pipeline {pipeline_id}: {e}")
            raise

    def list_pipeline_runs(
        self, pipeline_id: str, skip: int = 0, limit: int = 100
    ) -> List[PipelineRunResponse]:
        """List all runs for a pipeline"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            raise PipelineNotFoundError(pipeline_id)

        runs = (
            self.db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id)
            .order_by(PipelineRun.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [self._convert_to_response(run) for run in runs]

    def list_pipeline_runs_paginated(
        self, pipeline_id: str, page: int = 1, size: int = 100
    ) -> PaginationResponse[PipelineRunResponse]:
        """List pipeline runs with pagination"""
        pipeline = self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
        if not pipeline:
            raise PipelineNotFoundError(pipeline_id)

        skip = (page - 1) * size

        total = (
            self.db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id)
            .count()
        )

        runs = (
            self.db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id)
            .order_by(PipelineRun.created_at.desc())
            .offset(skip)
            .limit(size)
            .all()
        )

        items = [self._convert_to_response(run) for run in runs]

        return PaginationResponse.create(
            items=items,
            total=total,
            page=page,
            size=size,
        )

    def get_run_with_stages(
        self, pipeline_id: str, run_id: str
    ) -> Optional[PipelineRunWithStages]:
        """Get a pipeline run with all stage runs"""
        run = (
            self.db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id, PipelineRun.id == run_id)
            .first()
        )

        if not run:
            return None

        return self._convert_to_response_with_stages(run)

    def cancel_run(self, pipeline_id: str, run_id: str) -> bool:
        """Cancel a pipeline run"""
        run = (
            self.db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id, PipelineRun.id == run_id)
            .first()
        )

        if not run:
            return False

        try:
            run.status = RunStatus.CANCELLED
            run.completed_at = datetime.utcnow()
            run.execution_time = (
                (run.completed_at - run.started_at).total_seconds()
                if run.started_at
                else 0
            )

            for stage_run in run.stage_runs:
                if stage_run.status in [RunStatus.PENDING, RunStatus.RUNNING]:
                    stage_run.status = RunStatus.CANCELLED
                    stage_run.completed_at = datetime.utcnow()
                    if stage_run.started_at:
                        stage_run.execution_time = (
                            stage_run.completed_at - stage_run.started_at
                        ).total_seconds()

            self.db.commit()
            logger.info(f"Cancelled run {run_id}")
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to cancel run {run_id}: {e}")
            raise

    async def _simulate_execution(self, run_id: str):
        """Simulate pipeline execution with dummy data

        TODO: Implement actual execution logic here
        - Push events to a message queue (Kafka, RabbitMQ, etc.)
        - Create a worker pool to process the events
        - Process the events in the worker pool
        - Update the stage run status based on the event
        - Update the pipeline run status based on the stage run status
        - Update the pipeline run status based on the stage run status
        """
        try:
            await asyncio.sleep(1)

            run = self.db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
            if not run:
                return

            run.status = RunStatus.RUNNING
            self.db.commit()

            stages = sorted(run.stage_runs, key=lambda x: x.stage.order)

            for stage_run in stages:
                stage_run.status = RunStatus.RUNNING
                stage_run.started_at = datetime.utcnow()
                self.db.commit()

                execution_time = random.uniform(1, 5)
                await asyncio.sleep(execution_time)

                if random.random() < 0.9:
                    stage_run.status = RunStatus.COMPLETED

                    expected_artifacts = get_expected_artifact_types(
                        stage_run.stage.stage_type
                    )

                    stage_run.output_data = {
                        "result": f"Stage {stage_run.stage.name} completed successfully",
                        "stage_type": stage_run.stage.stage_type.value,
                        "custom_name": stage_run.stage.custom_name,
                        "expected_artifacts": [
                            artifact.value for artifact in expected_artifacts
                        ],
                    }
                    run.success_count += 1
                else:
                    stage_run.status = RunStatus.FAILED
                    stage_run.error_message = (
                        f"Simulated failure in stage {stage_run.stage.name}"
                    )
                    run.failed_count += 1

                stage_run.completed_at = datetime.utcnow()
                stage_run.execution_time = execution_time
                stage_run.memory_usage = random.uniform(100, 500)
                stage_run.cpu_usage = random.uniform(20, 80)

                self.db.commit()

                if stage_run.status == RunStatus.FAILED:
                    run.status = RunStatus.FAILED
                    run.error_message = (
                        f"Pipeline failed at stage: {stage_run.stage.name}"
                    )
                    break

            if run.status == RunStatus.RUNNING:
                run.status = RunStatus.COMPLETED
                run.output_data = {"message": "Pipeline completed successfully"}

            run.completed_at = datetime.utcnow()
            run.execution_time = (run.completed_at - run.started_at).total_seconds()
            run.max_memory_usage = max([sr.memory_usage or 0 for sr in run.stage_runs])
            run.max_cpu_usage = max([sr.cpu_usage or 0 for sr in run.stage_runs])

            self.db.commit()
            logger.info(f"Completed run {run.id} with status {run.status}")

        except Exception as e:
            logger.error(f"Error in simulated execution for run {run_id}: {e}")

    def _convert_to_response(self, run: PipelineRun) -> PipelineRunResponse:
        """Convert PipelineRun model to response schema"""
        return PipelineRunResponse(
            id=str(run.id),
            pipeline_id=str(run.pipeline_id),
            status=run.status,
            trigger_type=run.trigger_type,
            triggered_by=run.triggered_by,
            started_at=run.started_at,
            completed_at=run.completed_at,
            execution_time=run.execution_time,
            run_config=run.run_config,
            environment=run.environment,
            max_memory_usage=run.max_memory_usage,
            max_cpu_usage=run.max_cpu_usage,
            success_count=run.success_count,
            failed_count=run.failed_count,
            error_message=run.error_message,
            output_data=run.output_data,
            tags=run.tags,
            notes=run.notes,
            created_at=run.created_at,
            updated_at=run.updated_at,
        )

    def _convert_to_response_with_stages(
        self, run: PipelineRun
    ) -> PipelineRunWithStages:
        """Convert PipelineRun model to response schema with stage runs"""
        stage_responses = []
        for stage_run in run.stage_runs:
            stage_response = StageRunResponse(
                id=str(stage_run.id),
                pipeline_run_id=str(stage_run.pipeline_run_id),
                stage_id=str(stage_run.stage_id),
                status=stage_run.status,
                attempt_number=stage_run.attempt_number,
                started_at=stage_run.started_at,
                completed_at=stage_run.completed_at,
                execution_time=stage_run.execution_time,
                memory_usage=stage_run.memory_usage,
                cpu_usage=stage_run.cpu_usage,
                output_data=stage_run.output_data,
                error_message=stage_run.error_message,
                logs=stage_run.logs,
                created_at=stage_run.created_at,
                updated_at=stage_run.updated_at,
            )
            stage_responses.append(stage_response)

        stage_responses.sort(key=lambda x: x.stage_id)

        return PipelineRunWithStages(
            id=str(run.id),
            pipeline_id=str(run.pipeline_id),
            status=run.status,
            trigger_type=run.trigger_type,
            triggered_by=run.triggered_by,
            started_at=run.started_at,
            completed_at=run.completed_at,
            execution_time=run.execution_time,
            run_config=run.run_config,
            environment=run.environment,
            max_memory_usage=run.max_memory_usage,
            max_cpu_usage=run.max_cpu_usage,
            success_count=run.success_count,
            failed_count=run.failed_count,
            error_message=run.error_message,
            output_data=run.output_data,
            tags=run.tags,
            notes=run.notes,
            created_at=run.created_at,
            updated_at=run.updated_at,
            stage_runs=stage_responses,
        )
