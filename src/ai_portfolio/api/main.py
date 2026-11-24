"""FastAPI application factory and ASGI entrypoint."""

from typing import Annotated, Literal

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_portfolio import __version__
from ai_portfolio.config import Settings, get_settings
from ai_portfolio.utils.logging import configure_logging


class HealthResponse(BaseModel):
    """Service health metadata returned by `/health`."""

    status: Literal["ok"]
    app_name: str
    version: str
    environment: str


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    configure_logging(settings.log_level)

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Unified FastAPI serving layer for AI Engineer & Data Scientist projects.",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health", response_model=HealthResponse, tags=["health"])
    def health_check(
        current_settings: Annotated[Settings, Depends(get_settings)],
    ) -> HealthResponse:
        """Return service liveness and configuration summary."""
        return HealthResponse(
            status="ok",
            app_name=current_settings.app_name,
            version=__version__,
            environment=current_settings.environment,
        )

    # Mount portfolio project routers under `/api/v1/<project>`, for example:
    # from ai_portfolio.projects.<project_name>.router import router as project_router
    # application.include_router(project_router)

    return application


app = create_app()
