from app.repositories.base_user import BaseUserRepository
from app.schemas.user import ClientUserCreatePayload, UserQueryParams


class UserApdater:
    def __init__(self, repository: BaseUserRepository):
        self.repository = repository

    def get_user_by_id(self, user_id: str):
        return self.repository.get_user_by_id(user_id)

    def list_users(self, params: UserQueryParams):
        return self.repository.list_users(params)

    def create_user(self, payload: ClientUserCreatePayload):
        return self.repository.create_user(payload)
