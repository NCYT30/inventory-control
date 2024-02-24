from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from passlib.context import CryptContext
from passlib.hash import bcrypt

from ..schemas import UsersResponseModel
from ..schemas import UsersRequestModel
from ..schemas import UsersRequesPutModel

from ..database import Users


router = APIRouter(prefix = '/users')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get('/', response_model = list[UsersResponseModel])
async def get_users(page: int = 1, limit = 10):
    users = Users.select().where(Users.active == 0)

    return [ user for user in users]




@router.get('/{users_id}', response_model = UsersResponseModel)
async def get_user_id(users_id: int = Path(..., title = 'User  ID', ge = 1)):
    users = Users.get_or_none((Users.id == users_id) & (Users.active == 0))

    if users is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Users not found")
    
    return users

@router.post('/', response_model = UsersResponseModel)
async def create_users(users:  UsersRequestModel):

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
async def update_user(id: int, users_request: UsersRequesPutModel):
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
async def update_password_users(user_id: int, user_request: UsersRequesPutModel):

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
async def delete_user(id: int, users_request: UsersRequesPutModel):

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