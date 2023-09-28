import logging
from app.repositories.role import RoleRepository

logger = logging.getLogger(__name__)


class RoleService:
    def __init__(
        self,
        role_repository: RoleRepository,
    ):
        self.role_repository = role_repository

    def get_all_roles(self):
        return self.role_repository.find_all()

    def get_role_by_code(self, code: str):
        return self.role_repository.get_role_by_code(code)
