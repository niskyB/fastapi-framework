from typing import Any, Callable, Generic, Optional, TypeVar
from sqlalchemy.orm import Session
from app.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, entity: T, get_session: Callable[[], Session]):
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
