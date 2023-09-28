from app.repositories.azure_user import AzureUserRepository
from app.schemas.user import (
    ClientUserCreatePayload,
    ClientUserListResponse,
    ClientUserResponse,
    UserQueryParams,
)
from app.utils.user import create_user_request


class UserApdater:
    def __init__(self, repository: AzureUserRepository):
        self.repository = repository

    def get_user_by_id(self, user_id: str):
        return ClientUserResponse(**self.repository.get_user_by_id(user_id))

    def list_users(self, params: UserQueryParams):
        return ClientUserListResponse(**self.repository.list_users(params)).value

    def create_user(self, payload: ClientUserCreatePayload):
        user = self.repository.create_user(create_user_request(data=payload))
        return ClientUserResponse(**user.model_dump())
