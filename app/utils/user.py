from enum import Enum

from app.core import settings
from app.schemas.azure import AzureUserCreatePayload
from app.schemas.user import ClientUserCommonProps, ClientUserCreatePayload
from app.utils.string_utils import gen_password


class UserProperties(str, Enum):
    ID = "id"
    ACCOUNT_ENABLED = "accountEnabled"
    DISPLAY_NAME = "displayName"
    MAIL = "mail"
    MOBILE_PHONE = "mobilePhone"
    GIVEN_NAME = "givenName"
    CITY = "city"
    DEPARTMENT = "department"
    OFFICE_LOCATION = "officeLocation"
    JOB_TITLE = "jobTitle"
    OTHER_MAILS = "otherMails"
    USER_PRINCIPAL_NAME = "userPrincipalName"
    IDENTITIES = "identities"
    ROLES = f"{settings.EXTENSION_KEY_PREFIX}_roles"


def get_user_select_properties():
    select_properties = ""
    user_properties_list = list(UserProperties)

    for i, e in enumerate(user_properties_list):
        select_properties += f"{e.value}"
        if i < len(user_properties_list) - 1:
            select_properties += ","
    return select_properties


def create_user_request(data: ClientUserCreatePayload):
    """Create payload for creating user in Azure AD with email as sign-in type
    and a randomly generated password (that requires changing next sign-in).\n

    Args:
        data (LocalUserRequest): User data from request body

    Returns:
        dict: Create user payload.
    """
    payload = ClientUserCommonProps(**data.model_dump()).model_dump()
    payload.update(
        {
            "accountEnabled": data.enabled,
            f"{settings.EXTENSION_KEY_PREFIX}_roles": data.role,
            "displayName": data.displayName,
            "mail": data.mail,
            "identities": [
                {
                    "signInType": "emailAddress",
                    "issuer": f"{settings.TENANT_NAME}.onmicrosoft.com",
                    "issuerAssignedId": data.mail,
                },
            ],
            "passwordProfile": {
                "password": gen_password(),
                "forceChangePasswordNextSignIn": "true",
            },
            "passwordPolicies": "DisablePasswordExpiration",
            "creationType": "LocalAccount",
        }
    )
    return AzureUserCreatePayload(**payload)
