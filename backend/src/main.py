import uvicorn

from src.core.config import settings
from src.server import app

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers,
    )
