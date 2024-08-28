import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import router as api_endpoint_routers
from src.config.settings.base import config_env
from src.config.settings.logger_config import logger
from src.repository.database import Base, engine


def initialize_backend_application() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config_env.ALLOWED_ORIGINS,
        allow_credentials=config_env.IS_ALLOWED_CREDENTIALS,
        allow_methods=config_env.ALLOWED_METHODS,
        allow_headers=config_env.ALLOWED_HEADERS,
    )

    app.include_router(router=api_endpoint_routers)

    @app.on_event("startup")
    async def startup_event():
        """
        Function for application startup log and database initialization
        """
        logger.info("Application startup")
        # await create_tables()

    @app.on_event("shutdown")
    async def shutdown_event():
        """
        Function for application shutdown log
        """
        logger.info("Application shutdown")

    return app


backend_app: FastAPI = initialize_backend_application()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
