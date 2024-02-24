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


#----------INVENTORY-------------

class ProductValidator():

    @validator('product')
    def product_validator(cls, product):
        product: str
        if len(product) < 3 or len(product) > 25:
            raise ValueError('El rango para escribir el producto es 3 a 25 caracteres')
        
        return product



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
    total_value: int
    active: int


class InventoryRequestModel(ProductValidator, BaseModel):
    product: str
    sku: int
    ubication: str
    method: str
    detail: str
    amount: int
    unit_value: int
    active: int


class InventoryRequestPutModel(ProductValidator, BaseModel):
    product: str
    sku: int
    ubication: str
    method: str
    date: str
    detail: str
    amount: int
    unit_value: int
    total_value: int
    active: int


#------------Users-------------------



class UsersResponseModel(ResponseModel):
    id: int
    name: str
    surnames: str
    phone: int
    email: str
    password: str
    active: int


class UsersRequestModel(BaseModel):
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



#---------------Providers-------------------



class ProvidersResponseModel(ResponseModel):
    id: int
    name: str
    description: str
    addres: str
    email: str
    phone: int
    active: int


class ProvidersRequestModel(BaseModel):
    id: int
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

