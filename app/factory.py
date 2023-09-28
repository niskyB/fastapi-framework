from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1 import include_router
from app.core import settings
from app.core.containers import Container
from dependency_injector import providers
from azure.identity import ClientSecretCredential
from app.adapters.azure_user import AzureUserAdapter
from msgraph.core import APIVersion
from msgraph.core import GraphClient


class ExtendedFastAPI(FastAPI):
    def __init__(self, container: Container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container


def create_app() -> ExtendedFastAPI:
    graph_client_credential = providers.Singleton(
        ClientSecretCredential,
        tenant_id=settings.TENANT_ID,
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
    )

    graph_client = providers.Singleton(
        GraphClient,
        credential=graph_client_credential,
        api_version=APIVersion.beta,
    )

    container = Container(
        user_adapter=providers.Singleton(AzureUserAdapter, client=graph_client)
    )

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
