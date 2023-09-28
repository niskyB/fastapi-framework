import logging
from http import HTTPStatus
from fastapi import HTTPException
from msgraph.core import GraphClient
from app.constants.azure import AZURE_USERS_PATH
from app.schemas.azure import AzureUserCreatePayload, AzureUserCreateResponse
from app.schemas.user import UserQueryParams
from app.utils.user import get_user_select_properties

logger = logging.getLogger(__name__)


class AzureUserRepository:
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
        return res.json()

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

        return res.json()

    def create_user(self, payload: AzureUserCreatePayload):
        """Send request to Azure AD to create new user.\n

        Args:
            payload (dict): User payload.

        Raises:
            HTTPException: Something went wrong while creating user.

        Returns:
            dict: Created user object.
        """
        response = self.client.post(
            url=AZURE_USERS_PATH,
            data=payload.model_dump_json(exclude_none=True, by_alias=True),
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != HTTPStatus.CREATED:
            logger.error(response.json())
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )
        return AzureUserCreateResponse(**response.json())
