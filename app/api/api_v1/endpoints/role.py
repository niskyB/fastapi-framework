from fastapi import APIRouter, Depends, Path, status
from app.services import RoleService
from dependency_injector.wiring import inject, Provide
from app.core.containers import Container

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
@inject
async def list_roles(
    role_service: RoleService = Depends(Provide[Container.role_service]),
):
    return role_service.get_all_roles()


@router.get("/{code}", status_code=status.HTTP_200_OK)
@inject
async def get_role_by_id(
    code: str = Path(..., nullable=False),
    role_service: RoleService = Depends(Provide[Container.role_service]),
):
    return role_service.get_role_by_code(code=code)
