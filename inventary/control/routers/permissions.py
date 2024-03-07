from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, status, Depends

from ..schemas import PermissionsResponseModel
from ..schemas import PermissionsRequestModel
from ..schemas import PermissionsRequestPutModel

from ..database import Permissions
from ..database import RolPer, Users

from .login import get_current_user



router = APIRouter(prefix = '/permissions')

@router.get('/', response_model = list[PermissionsResponseModel])
async def get_permissions(page: int = 1, limit: int = 10, current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=7)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a permisos")


    permissions = Permissions.select()

    return [ permission for permission in permissions ]
    

@router.post('/', response_model = PermissionsResponseModel)
async def create_permissions(permissions: PermissionsRequestModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=7)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a permisos")


    permission = Permissions.create(
        name = permissions.name
    )

    return permission


@router.put('/{id}', response_model = PermissionsResponseModel)
async def update_permissions(id: int, permissions_request: PermissionsRequestPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=7)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a permisos")


    permission = Permissions.select().where(Permissions.id == id).first()

    if permission is None:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = 'Permissions not found')

    permission.name = permissions_request.name

    permission.save()

    return permission



@router.delete('/{id}', response_model = PermissionsResponseModel)
async def delete_permissions(id: int,  current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=7)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a permisos")


    permission = Permissions.select().where(Permissions.id == id).first()

    if permission is None:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = 'Permissions not found')
    

    permission.delete_instance()

    return permission