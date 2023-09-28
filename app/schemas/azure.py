from typing import Optional
from pydantic import Field, validator
from app.schemas.user import ClientUserCommonProps, PasswordProfile
from app.core import settings


class AzureUserCreatePayload(ClientUserCommonProps):
    passwordProfile: Optional[PasswordProfile] = None
    passwordPolicies: Optional[str] = None
    creationType: Optional[str] = None
    role: Optional[str] = Field(
        default=None, alias=f"{settings.EXTENSION_KEY_PREFIX}_roles"
    )

    @validator("*")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
