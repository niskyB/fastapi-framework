from typing import List, Optional
from fastapi import HTTPException, Query, status
from pydantic import BaseModel, EmailStr, validator
from typing_extensions import Annotated
from app.core import settings
from app.constants.error_message import INVALID_ROLE
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal


class Identity(BaseModel):
    signInType: Literal["emailAddress", "userName", "userPrincipalName", "federated"]
    issuer: str
    issuerAssignedId: Optional[str]


class UserQueryParams(BaseModel):
    value: Annotated[str, Query()] = ""


class BaseUser(BaseModel):
    mobilePhone: Optional[str] = None
    givenName: Optional[str] = None
    city: Optional[str] = None
    department: Optional[str] = None
    officeLocation: Optional[str] = None
    jobTitle: Optional[str] = None
    otherMails: List[EmailStr] = []


class PasswordProfile(BaseModel):
    forceChangePasswordNextSignIn: bool = True
    forceChangePasswordNextSignInWithMfa: bool = False
    password: str


class ClientUserCommonProps(BaseModel):
    accountEnabled: bool = True
    identities: List[Identity] = []
    role: Optional[str] = None
    displayName: Optional[str] = None
    mail: Optional[EmailStr] = None
    mobilePhone: Optional[str] = None
    givenName: Optional[str] = None
    city: Optional[str] = None
    department: Optional[str] = None
    officeLocation: Optional[str] = None
    jobTitle: Optional[str] = None
    otherMails: List[EmailStr] = []


class ClientUserResponse(ClientUserCommonProps):
    id: str
    userPrincipalName: str


class ClientUserListResponse(BaseModel):
    value: List[ClientUserResponse]
    nextLink: Optional[str] = Field(default=None, alias="@odata.nextLink")


class ClientUserCreatePayload(BaseUser):
    mail: EmailStr
    role: str
    displayName: str = ""
    enabled: bool = True

    @validator("role")
    def validate_role(cls, v):
        if v not in settings.USER_ROLES.model_dump().values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_ROLE
            )
        return v
