from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1 import include_router
from app.core import settings
from app.core.containers import Container


class ExtendedFastAPI(FastAPI):
    def __init__(self, container: Container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container


def create_app() -> ExtendedFastAPI:
    container = Container()

    app = ExtendedFastAPI(container=container)

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    include_router(app)

    return app
