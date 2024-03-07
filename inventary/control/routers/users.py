from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import Depends, status

from passlib.context import CryptContext
from passlib.hash import bcrypt

from ..schemas import UsersResponseModel
from ..schemas import UsersRequestModel
from ..schemas import UsersRequesPutModel

from .login import get_current_user

from ..database import Users, RolPer


router = APIRouter(prefix = '/users')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/', response_model=List[UsersResponseModel])
async def get_users(current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")


    users = Users.select().where(Users.active == 0)
    return [user for user in users]



@router.get('/{users_id}', response_model = UsersResponseModel)
async def get_user_id(users_id: int = Path(..., title = 'User  ID', ge = 1),current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")

    users = Users.get_or_none((Users.id == users_id) & (Users.active == 0))

    if users is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Users not found")
    
    return users

@router.post('/', response_model = UsersResponseModel)
async def create_users(users:  UsersRequestModel, current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")

    hashed_password = bcrypt.hash(users.password)

    users = Users.create(
        name = users.name,
        surnames = users.surnames,
        phone = users.phone,
        email = users.email,
        password = hashed_password,
        active = 0
    )

    return users
 

@router.put('/{id}', response_model=UsersResponseModel)
async def update_user(id: int, users_request: UsersRequesPutModel, current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")


    users = Users.select().where(Users.id == id).first()

    if users is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    if users.active == 1:  
        raise HTTPException(status_code=403, detail='No se puede editar un usuario inactivo')

    users.name = users_request.name
    users.surnames = users_request.surnames
    users.phone = users_request.phone
    users.email = users_request.email
    users.password = users_request.password

    users.save()

    return users



@router.put('/pass/{user_id}', response_model=UsersResponseModel)
async def update_password_users(user_id: int, user_request: UsersRequesPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")


    user = Users.select().where(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    if user.active == 1:  
        raise HTTPException(status_code=403, detail='No se puede editar un usuario inactivo')

    # Obtén la contraseña encriptada
    hashed_password = get_password_hash(user_request.password)

    # Actualiza la contraseña en la base de datos
    user.password = hashed_password
    
    user.save()

    return user



@router.delete('/{id}', response_model = UsersResponseModel)
async def delete_user(id: int, users_request: UsersRequesPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=2)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al usuario")


    users = Users.select().where(Users.id == id).first()

    if users is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    users.active = 1

    users.save()

    return users

def get_password_hash(password: str):
    # Configura el contexto de cifrado
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Hashea la contraseña
    return pwd_context.hash(password)