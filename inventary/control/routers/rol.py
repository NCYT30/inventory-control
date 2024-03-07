from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, status, Depends

from ..schemas import RolResponseModel
from ..schemas import RolRequestModel
from ..schemas import RolRequestPutModel

from ..database import RolPer
from ..database import Permissions
from ..database import Users

from .login import get_current_user


router = APIRouter(prefix = '/rol')


@router.get('/', response_model = list[RolResponseModel])
async def get_rol(page: int = 1, limit: int  = 10, current_user: Users = Depends(get_current_user)):

    user = await current_user  

    permission = RolPer.get_or_none(fk_user=user.id, fk_per=8)
    
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a roles")



    rol =  RolPer.select()

    return [ ro for ro in rol ]


@router.post('/', response_model=RolResponseModel)
async def create_rol(rol: RolRequestModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  

    permission = RolPer.get_or_none(fk_user=user.id, fk_per=8)

    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a roles")



    permissions = Permissions.select().where(Permissions.id == rol.fk_per.id).first()

    users = Users.select().where(Users.id == rol.fk_user.id).first() 


    if permissions is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Permissions not found' ) 

    if users is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Users not found')

    rol = RolPer.create(
        fk_per = rol.fk_per.id,
        fk_user = rol.fk_user.id
    )

    return rol


@router.put('/{id}', response_model = RolRequestPutModel)
async def update_rol(id: int, roles_request: RolRequestPutModel, current_user: Users = Depends(get_current_user)):


    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=8)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a roles")



    rol = RolPer.select().where(RolPer.id == id).first()

    permissions = Permissions.select().where(Permissions.id == roles_request.fk_per.id).first()

    users = Users.select().where(Users.id == roles_request.fk_user.id).first() 

    if rol is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Rol not found')
    
    if permissions is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Permissions not found' ) 

    if users is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Users not found')

    rol.fk_per = roles_request.fk_per.id
    rol.fk_user = roles_request.fk_user.id

    rol.save()

    return  rol