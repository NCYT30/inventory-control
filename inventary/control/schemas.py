from typing import Any

from datetime import date

from pydantic import validator
from pydantic import BaseModel

from pydantic.utils import GetterDict

from peewee import ModelSelect

class PeeWeeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res 


class ResponseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeWeeGetterDict




#------------Users-------------------

class UserValidator:

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 25:
            raise ValueError('El rango para escribir el nombre es de 3 a 25 caracteres')
        return name

    @validator('surnames')
    def surnames_validator(cls, surnames):
        if len(surnames) < 3 or len(surnames) > 25:
            raise ValueError('El rango para escribir los apellidos es de 3 a 25 caracteres')
        return surnames

    @validator('phone')
    def phone_validator(cls, phone):
        if len(str(phone)) != 10:
            raise ValueError('El número de teléfono debe tener 10 dígitos')
        return phone

    @validator('email')
    def email_validator(cls, email):
        if '@' not in email or '.' not in email:
            raise ValueError('El correo electrónico no tiene un formato válido')
        return email

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 6 or len(password) > 20:
            raise ValueError('La contraseña debe tener entre 6 y 20 caracteres')
        return password

class UsersResponseModel(ResponseModel):
    id: int
    name: str
    surnames: str
    phone: int
    email: str
    password: str
    active: int


class UsersRequestModel(BaseModel, UserValidator):
    name: str
    surnames: str
    phone: int
    email: str
    password: str
    active: int

class UsersRequesPutModel(BaseModel):
    name: str
    surnames: str
    phone: int
    email: str
    password: str
    active: int


#-------------CATEGORY-----------------

class CategoryValidator:

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 25:
            raise ValueError('El rango para escribir el nombre es de 3 a 25 caracteres')
        return name


class CategoryResponseModel(ResponseModel):
    id: int
    name: str


class CategoryRequestModel(BaseModel, CategoryValidator):
    name: str


class CategoryPutModel(BaseModel, CategoryValidator):
    name: str



#----------INVENTORY-------------



class InventoryValidator:

    @validator('product')
    def product_validator(cls, product):
        if len(product) < 3 or len(product) > 25:
            raise ValueError('El rango para escribir el producto es de 3 a 25 caracteres')
        return product

    @validator('ubication')
    def ubication_validator(cls, ubication):
        if len(ubication) < 3 or len(ubication) > 25:
            raise ValueError('El rango para escribir la ubicación es de 3 a 25 caracteres')
        return ubication

    @validator('method')
    def method_validator(cls, method):
        if len(method) < 3 or len(method) > 25:
            raise ValueError('El rango para escribir el método es de 3 a 25 caracteres')
        return method

    @validator('detail')
    def detail_validator(cls, detail):
        if len(detail) < 3 or len(detail) > 25:
            raise ValueError('El rango para escribir el detalle es de 3 a 25 caracteres')
        return detail

class InventoryResponseModel(ResponseModel):
    id: int
    product: str
    sku: int
    ubication: str
    method: str
    date: str
    detail: str
    amount: int
    unit_value: int
    fk_category: CategoryResponseModel
    fk_user: UsersResponseModel
    active: int


class InventoryRequestModel(InventoryValidator, BaseModel):
    product: str
    sku: int
    ubication: str
    method: str
    detail: str
    amount: int
    unit_value: int
    fk_category: CategoryResponseModel
    active: int


class InventoryRequestPutModel(InventoryValidator, BaseModel):
    product: str
    sku: int
    ubication: str
    method: str
    detail: str
    amount: int
    unit_value: int
    fk_category: CategoryResponseModel
    active: int




#---------------PROVIDERS-------------------

class ProvidersValidator:

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 25:
            raise ValueError('El rango para escribir el nombre es de 3 a 25 caracteres')
        return name

    @validator('description')
    def description_validator(cls, description):
        if len(description) < 3 or len(description) > 25:
            raise ValueError('El rango para escribir la descripción es de 3 a 25 caracteres')
        return description

    @validator('addres')
    def addres_validator(cls, addres):
        if len(addres) < 3 or len(addres) > 25:
            raise ValueError('El rango para escribir la dirección es de 3 a 25 caracteres')
        return addres

    @validator('phone')
    def phone_validator(cls, phone):
        if len(str(phone)) != 10:
            raise ValueError('El número de teléfono debe tener 10 dígitos')
        return phone


class ProvidersResponseModel(ResponseModel):
    id: int
    name: str
    description: str
    addres: str
    email: str
    phone: int
    fkusr: UsersResponseModel
    active: int


class ProvidersRequestModel(BaseModel, ProvidersValidator):
    name: str
    description: str
    addres: str
    email: str
    phone: int
    active: int



class ProvidersPutModel(BaseModel):
    name: str
    description: str
    addres: str
    email: str
    phone: int
    active: int


#------------SALES---------------

class SalesResponseModel(ResponseModel):
    fk_inv: InventoryResponseModel
    amount: int
    total_value: int


class SalesRequestModel(BaseModel):
    fk_inv: InventoryResponseModel
    amount: int
    total_value: int


class SalesRequestPutModel(BaseModel):
    fk_inv: InventoryResponseModel
    amount: int



#-------------PERMISSIONS------------

class PermissionsResponseModel(ResponseModel):
    id: int
    name: str


class PermissionsRequestModel(BaseModel):
    name: str


class PermissionsRequestPutModel(BaseModel):
    name: str


#----------ROLPER-------------------


class RolResponseModel(ResponseModel):
    id: int
    fk_per: PermissionsResponseModel
    fk_user: UsersResponseModel


class RolRequestModel(BaseModel):
    fk_per: PermissionsResponseModel
    fk_user: UsersResponseModel


class RolRequestPutModel(BaseModel):
    fk_per: PermissionsResponseModel
    fk_user: UsersResponseModel