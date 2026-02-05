# third party imports
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router

# within app imports
from app.config import settings
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    """
    # Startup
    setup_logging()
    print("🚀Starting...")

    yield

    # Shutdown
    print("Shutting down...")


def create_app() -> FastAPI:
    """application instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Middleware
    setup_middleware(app)

    # Routers
    app.include_router(api_v1_router, prefix="/api/v1")

    # entrypoint
    @app.get("/")
    async def root():
        return {"message": "Hello world!"}

    # health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "environment": settings.ENVIRONMENT}

    return app


def run():
    uvicorn.run(
        "app.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        factory=True,
    )


app = create_app()

if __name__ == "__main__":
    run()
