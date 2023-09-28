import logging
import yaml
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.role import Role
from app.schemas.role import Role as RoleSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        with open(settings.ROLES_YML_FILE, "r") as file:
            roles = RoleSchema(**yaml.safe_load(file)["user_roles"])

        system_roles = db.query(Role).all()
        role_codes = [role.code for role in system_roles]
        for key in list(roles.model_dump().keys()):
            if roles.model_dump()[key] in role_codes:
                continue
            db.add(Role(name=key, code=roles.model_dump()[key]))
        db.commit()
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()


def main() -> None:
    logger.info("Starting migration")
    init()
    logger.info("Migration finished")


if __name__ == "__main__":
    main()
