from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from app.core.containers import Container
from app.schemas.user import ClientUserCreatePayload, UserQueryParams
from app.services import UserService

router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@inject
def get_user_by_id(
    user_id: str = Path(..., nullable=False),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_user_by_id(user_id=user_id)


@router.get("", status_code=status.HTTP_200_OK)
@inject
def list_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
    params: UserQueryParams = Depends(UserQueryParams),
):
    return user_service.list_users(params)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_local_user(
    data: ClientUserCreatePayload,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user(data)
