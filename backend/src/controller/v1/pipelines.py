from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.exceptions import PipelineNotFoundError, PipelineValidationError
from src.models.dto import (
    PaginationResponse,
    PipelineCreate,
    PipelineResponse,
    PipelineWithStages,
)
from src.services.pipeline_service import PipelineService

pipeline_router = APIRouter(prefix="/pipelines", tags=["Pipelines"])


@pipeline_router.post(
    "/", response_model=PipelineWithStages, status_code=status.HTTP_201_CREATED
)
async def create_pipeline(pipeline_data: PipelineCreate, db: Session = Depends(get_db)):
    """Register a new ML pipeline with its stages"""
    try:
        service = PipelineService(db)
        pipeline = service.create_pipeline(pipeline_data)
        return pipeline
    except PipelineValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create pipeline: {str(e)}"
        )


@pipeline_router.get("/", response_model=PaginationResponse[PipelineResponse])
async def list_pipelines(page: int = 1, size: int = 100, db: Session = Depends(get_db)):
    """List all registered pipelines with pagination"""
    try:
        service = PipelineService(db)
        pipelines = service.list_pipelines_paginated(page=page, size=size)
        return pipelines
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list pipelines: {str(e)}"
        )


@pipeline_router.get("/{pipeline_id}", response_model=PipelineWithStages)
async def get_pipeline(pipeline_id: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific pipeline"""
    try:
        service = PipelineService(db)
        pipeline = service.get_pipeline_with_stages(pipeline_id)
        if not pipeline:
            raise PipelineNotFoundError(pipeline_id)
        return pipeline
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pipeline: {str(e)}")


@pipeline_router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline(pipeline_id: str, db: Session = Depends(get_db)):
    """Delete a pipeline and all its associated data"""
    try:
        service = PipelineService(db)
        success = service.delete_pipeline(pipeline_id)
        if not success:
            raise PipelineNotFoundError(pipeline_id)
    except PipelineNotFoundError:
        raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete pipeline: {str(e)}"
        )
