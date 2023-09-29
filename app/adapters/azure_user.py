import logging
from http import HTTPStatus
from fastapi import HTTPException
from msgraph.core import GraphClient
from app.adapters.user_adapter import UserApdater
from app.constants.azure import AZURE_USERS_PATH
from app.schemas.azure import AzureUserResponse
from app.schemas.user import (
    ClientUserCreatePayload,
    ClientUserListResponse,
    UserQueryParams,
)
from app.utils.user import create_user_request, get_user_select_properties

logger = logging.getLogger(__name__)


class AzureUserAdapter(UserApdater):
    def __init__(self, client: GraphClient):
        self.client = client

    def get_user_by_id(self, user_id: str):
        """Get user by id/userPrincipalName from Azure AD. If user not found, raise HTTPException.\n
        Args:
            `user_id` (str): id or principal name of user.\n
            `client` (CustomGraphClient): MSGraph client.\n
        Raises:
            HTTPException: User not found or something went wrong while getting user.
        Returns:
            AzureUserResponse: User object.
        """

        res = self.client.get(
            f"{AZURE_USERS_PATH}/{user_id}?$select={get_user_select_properties()}"
        )

        if res.status_code != HTTPStatus.OK:
            logger.error(res.json().get("error").get("message"))
            raise HTTPException(
                res.status_code, detail=res.json().get("error").get("message")
            )
        return AzureUserResponse(**res.json()).model_dump()

    def list_users(self, params: UserQueryParams):
        """Get all users from Azure AD.\n

        Args:
            `params` (UserQueryParams): params for filtering users.\n
            `client` (CustomGraphClient): MSGraph client.\n

        Raises:
            HTTPException: Something went wrong while getting users.

        Returns:
            List[AzureUserResponse]: List of users.
        """
        url = f"{AZURE_USERS_PATH}?$select={get_user_select_properties()}"
        if params.value:
            url += f"&$filter=startsWith(mail, '{params.value}') OR startsWith(displayName, '{params.value}')"
        res = self.client.get(url)

        if res.status_code != HTTPStatus.OK:
            logger.error(res.json().get("error").get("message"))
            raise HTTPException(res.status_code, res.json().get("error").get("message"))

        return ClientUserListResponse(**res.json()).value

    def create_user(self, payload: ClientUserCreatePayload):
        """Send request to Azure AD to create new user.\n

        Args:
            payload (dict): User payload.

        Raises:
            HTTPException: Something went wrong while creating user.

        Returns:
            dict: Created user object.
        """
        data = create_user_request(payload)
        response = self.client.post(
            url=AZURE_USERS_PATH,
            data=data.model_dump_json(exclude_none=True, by_alias=True),
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != HTTPStatus.CREATED:
            logger.error(response.json())
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )
        return AzureUserResponse(**response.json()).model_dump()
