from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controller import router
from src.core.config import settings
from src.core.database import init_database
from src.core.exceptions import APIException


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_exception_handlers(app_: FastAPI) -> None:
    @app_.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_type": exc.error_type},
        )

    @app_.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error_type": "internal_error"},
        )


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=settings.effective_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app_)
    init_exception_handlers(app_)

    return app_


app = create_app()
