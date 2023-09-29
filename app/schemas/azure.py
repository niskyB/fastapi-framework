from typing import Optional
from pydantic import Field, validator
from app.schemas.user import ClientUserCommonProps, ClientUserResponse, PasswordProfile
from app.core import settings


class AzureUserCommon(ClientUserCommonProps):
    role: Optional[str] = Field(
        default=None, alias=f"{settings.EXTENSION_KEY_PREFIX}_roles"
    )


class AzureUserCreatePayload(AzureUserCommon):
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


class AzureUserResponse(ClientUserResponse):
    role: Optional[str] = Field(
        default=None, alias=f"{settings.EXTENSION_KEY_PREFIX}_roles"
    )

    @validator("*")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
