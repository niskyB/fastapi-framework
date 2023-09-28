from dependency_injector import containers, providers
from app.adapters.user_adapter import UserApdater
from app.core import settings
from app.db.database import Database
from app.repositories.role import RoleRepository
from app.services.user import UserService
from app.services.role import RoleService


# Please import Container class directly from this file if you want to use it in another file.
# Don't import it from __init__.py in the "core" folder.
# This is for the pytest to run.
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.api_v1.endpoints.user",
            "app.api.api_v1.endpoints.role",
        ]
    )

    db = providers.Singleton(Database, db_url=settings.SQLALCHEMY_DATABASE_URL)

    user_adapter = providers.Dependency(instance_of=UserApdater)

    role_repository = providers.Factory(
        RoleRepository, get_session=db.provided.get_session
    )

    user_service = providers.Factory(
        UserService,
        user_adapter=user_adapter,
    )

    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository,
    )
