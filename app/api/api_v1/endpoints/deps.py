import logging
from typing import List
import jwt

from fastapi import HTTPException, Request, status
from app.constants.error_message import NO_TOKEN_PROVIDED, FORBIDDEN
from app.constants.header import HEADER_AUTHORIZATION
from app.core import settings
from app.schemas.token_claims import TokenClaims


logger = logging.getLogger(__name__)


def guard(request: Request, accepted_roles: List[str]):
    token = request.headers.get(HEADER_AUTHORIZATION)
    if not token or token.split()[0] != "Bearer":
        logger.error(NO_TOKEN_PROVIDED)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=NO_TOKEN_PROVIDED
        )
    try:
        json_data = jwt.decode(
            token.replace("Bearer ", ""), options={"verify_signature": False}
        )
        token_claims: TokenClaims = TokenClaims(**json_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    for role in accepted_roles:
        if role == token_claims.extension_roles:
            return token_claims

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=FORBIDDEN)


def customer_guard(request: Request):
    return guard(request, [settings.USER_ROLES.customer])
