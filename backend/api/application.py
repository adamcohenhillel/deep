"""Deeper 2022, All Rights Reserved
"""
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRouter

from api.lifetime import register_shutdown_event, register_startup_event

from api.users.views import users_router

def get_app() -> FastAPI:
    """Get api application
    """
    app = FastAPI(
        title="deeper2",
        description="Skip this for now",
        # version=metadata.version("deeper2"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    api_router = APIRouter()
    api_router.include_router(users_router, prefix='/users', tags=['users'])
    app.include_router(router=api_router, prefix='/api')

    return app
