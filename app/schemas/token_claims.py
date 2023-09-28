from typing import Optional
from pydantic import BaseModel, EmailStr


class TokenClaims(BaseModel):
    oid: Optional[str] = None
    sub: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    extension_roles: Optional[str] = None
    tfp: Optional[str] = None
    scp: Optional[str] = None
    azp: Optional[str] = None
    aud: Optional[str] = None
    iss: Optional[str] = None
    emails: list[EmailStr] = []
