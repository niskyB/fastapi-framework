import logging
from app.models import Role
from app.constants.error_message import SOMETHING_WENT_WRONG
from app.repositories.base_db import BaseRepository
from fastapi import HTTPException, status


logger = logging.getLogger(__name__)


class RoleRepository(BaseRepository[Role]):
    def __init__(self, get_session):
        super().__init__(entity=Role, get_session=get_session)

    def get_role_by_code(self, code: str):
        with self.get_session() as session:
            try:
                role: Role = session.query(Role).filter(Role.code == code).first()
                return role
            except Exception as e:
                logger.error(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=SOMETHING_WENT_WRONG,
                )
