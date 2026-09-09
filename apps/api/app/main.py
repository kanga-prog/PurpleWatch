"""FastAPI application entry point."""

from fastapi import FastAPI

from app.config import get_settings


def create_app() -> FastAPI:
    """Create and configure the PurpleWatch API."""

    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
    )

    @application.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        """Return the deterministic API health contract."""

        return {
            "status": "ok",
            "service": settings.service_name,
            "version": settings.version,
            "environment": settings.environment,
        }

    return application


app = create_app()
