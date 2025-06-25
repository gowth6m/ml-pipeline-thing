from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.exceptions import PipelineNotFoundError, PipelineRunNotFoundError
from src.models.dto import (
    PaginationResponse,
    PipelineRunResponse,
    PipelineRunWithStages,
    TriggerRunRequest,
)
from src.services.run_service import RunService

run_router = APIRouter(tags=["Pipeline Runs"])


@run_router.post(
    "/pipelines/{pipeline_id}/trigger_run",
    response_model=PipelineRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def trigger_pipeline_run(
    pipeline_id: str, trigger_data: TriggerRunRequest, db: Session = Depends(get_db)
):
    """Start a new pipeline run"""
    try:
        service = RunService(db)
        run = service.trigger_run(pipeline_id, trigger_data)
        return run
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger run: {str(e)}")


@run_router.get(
    "/pipelines/{pipeline_id}/runs",
    response_model=PaginationResponse[PipelineRunResponse],
)
async def list_pipeline_runs(
    pipeline_id: str, page: int = 1, size: int = 100, db: Session = Depends(get_db)
):
    """List all runs for a specific pipeline with pagination"""
    try:
        service = RunService(db)
        runs = service.list_pipeline_runs_paginated(pipeline_id, page=page, size=size)
        return runs
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list runs: {str(e)}")


@run_router.get(
    "/pipelines/{pipeline_id}/runs/{run_id}", response_model=PipelineRunWithStages
)
async def get_pipeline_run(
    pipeline_id: str, run_id: str, db: Session = Depends(get_db)
):
    """Get detailed information about a specific pipeline run"""
    try:
        service = RunService(db)
        run = service.get_run_with_stages(pipeline_id, run_id)
        if not run:
            raise PipelineRunNotFoundError(run_id)
        return run
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except PipelineRunNotFoundError:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get run: {str(e)}")


@run_router.delete(
    "/pipelines/{pipeline_id}/runs/{run_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def cancel_pipeline_run(
    pipeline_id: str, run_id: str, db: Session = Depends(get_db)
):
    """Cancel a running pipeline"""
    try:
        service = RunService(db)
        success = service.cancel_run(pipeline_id, run_id)
        if not success:
            raise PipelineRunNotFoundError(run_id)
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except PipelineRunNotFoundError:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel run: {str(e)}")
