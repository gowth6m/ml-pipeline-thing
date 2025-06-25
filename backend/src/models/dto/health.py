from datetime import datetime
from typing import Any, Dict

from ..core import CoreModel


class MemoryUsage(CoreModel):
    """Memory usage model"""

    used: str
    available: str
    percent: str


class HealthCheck(CoreModel):
    """Health check response model"""

    status: str = "healthy"
    version: str
    database: str = "connected"
    uptime: float
    environment: str
    timestamp: datetime
    memory_usage: MemoryUsage
