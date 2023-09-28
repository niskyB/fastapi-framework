import logging
import yaml
import os
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.role import Role
from app.schemas.role import Role as RoleSchema
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

create_schema_sql = text(f'CREATE SCHEMA IF NOT EXISTS "{settings.POSTGRES_SCHEMA}"')


def transfer_roles(roles: List[Role]):
    user_roles = {}
    for role in roles:
        user_roles[role.name] = role.code
    return RoleSchema(**user_roles)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Try to create schema to check if DB is awake
        db.execute(create_schema_sql)
        db.commit()
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()


def main() -> None:
    logger.info("Initializing schema")
    init()
    logger.info("Schema finished initializing")


if __name__ == "__main__":
    main()
