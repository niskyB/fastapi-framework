import logging
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base(metadata=MetaData(schema=settings.DB_SCHEMA))


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def get_session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
