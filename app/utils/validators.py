import logging
import re

from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError

from app.constants import PASSWORD_COMPLEXITY_ERROR

logger = logging.getLogger(__name__)


def validate_password(passwd: str):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&.]{8,}$"

    pattern = re.compile(reg)
    matched = re.search(pattern, passwd)

    if not matched:
        logger.error(PASSWORD_COMPLEXITY_ERROR)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=PASSWORD_COMPLEXITY_ERROR
        )

    return passwd


def is_email_valid(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
