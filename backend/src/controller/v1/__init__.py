from fastapi import APIRouter

from src.controller.v1.pipelines import pipeline_router
from src.controller.v1.runs import run_router

v1_router = APIRouter()
v1_router.include_router(pipeline_router)
v1_router.include_router(run_router)
