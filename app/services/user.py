import logging
from app.adapter.user_adapter import UserApdater
from app.schemas.user import ClientUserCreatePayload, UserQueryParams

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_adapter: UserApdater):
        self.user_adapter = user_adapter

    def get_user_by_id(self, user_id: str):
        return self.user_adapter.get_user_by_id(user_id)

    def list_users(self, params: UserQueryParams):
        return self.user_adapter.list_users(params)

    def create_user(self, payload: ClientUserCreatePayload):
        return self.user_adapter.create_user(payload)
