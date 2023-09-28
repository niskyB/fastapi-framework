from typing import Any, Generic, Optional, TypeVar

from app.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, entity: T, get_session):
        self.entity = entity
        self.get_session = get_session

    def find_all(self):
        with self.get_session() as session:
            return session.query(self.entity).all()

    def find_by_field(
        self,
        field: str,
        value: Any,
    ) -> Optional[T]:
        with self.get_session() as session:
            return (
                session.query(self.entity)
                .filter(getattr(self.entity, field) == value)
                .first()
            )
