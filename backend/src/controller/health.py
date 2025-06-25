import time
from datetime import datetime

import psutil
from fastapi import APIRouter, status
from sqlalchemy import text

from src.core.config import settings
from src.core.database.database import get_db
from src.models.dto.health import HealthCheck, MemoryUsage

router = APIRouter()


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=HealthCheck, tags=["Health"]
)
async def health_check():
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        database = "connected"
    except Exception as e:
        database = f"failed: {str(e)}"

    return HealthCheck(
        status="healthy",
        version=settings.version,
        database=database,
        uptime=time.time(),
        timestamp=datetime.now(),
        environment=settings.environment,
        memory_usage=MemoryUsage(
            used=f"{round(psutil.virtual_memory().used / 1024 / 1024, 2)} MB",
            available=f"{round(psutil.virtual_memory().available / 1024 / 1024, 2)} MB",
            percent=f"{psutil.virtual_memory().percent}%",
        ),
    )
