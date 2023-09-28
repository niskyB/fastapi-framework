from abc import ABC, abstractmethod
from app.schemas.user import (
    ClientUserCreatePayload,
    ClientUserListResponse,
    ClientUserResponse,
    UserQueryParams,
)


class BaseUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> ClientUserResponse:
        pass

    @abstractmethod
    def list_users(self, params: UserQueryParams) -> ClientUserListResponse:
        pass

    @abstractmethod
    def create_user(self, payload: ClientUserCreatePayload) -> ClientUserResponse:
        pass
