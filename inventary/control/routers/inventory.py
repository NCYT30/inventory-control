from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, status, Depends

from datetime import datetime

from ..schemas import InventoryResponseModel
from ..schemas import InventoryRequestModel
from ..schemas import InventoryRequestPutModel

from ..database import Inventory
from ..database import Category
from ..database import Users, RolPer

from .login import get_current_user

router = APIRouter(prefix='/inventory')

@router.get('/', response_model=list[InventoryResponseModel])
async def get_inventory(current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=3)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al inventario")

    inventory = Inventory.select().where(Inventory.active == 0)

    return [inv for inv in inventory]



@router.get('/{inventory_id}', response_model = InventoryResponseModel)
async def get_inventory_id(inventory_id: int = Path(..., title = 'Inventory  ID', ge = 1), current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=3)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al inventario")


    inventory = Inventory.get_or_none((Inventory.id == inventory_id) & (Inventory.active == 0))
    

    if inventory is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Inventory not found")
    
    return inventory


@router.post('/', response_model = InventoryResponseModel)
async def create_inventory(inventory: InventoryRequestModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=3)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al inventario")


    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    category = Category.select().where(Category.id == inventory.fk_category.id).first()


    if category is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Category not found')

    inventory = Inventory.create(
        product = inventory.product,
        sku = inventory.sku,
        ubication = inventory.ubication,
        method = inventory.method,
        date = formatted_date,
        detail = inventory.detail,
        amount = inventory.amount,
        unit_value = inventory.unit_value,
        fk_category = inventory.fk_category.id,
        fk_user = user.id,
        active = 0
    )

    return inventory


@router.put('/{id}', response_model=InventoryResponseModel)
async def update_inventory(id: int, inventory_request: InventoryRequestPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=3)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al inventario")


    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    inventory = Inventory.select().where(Inventory.id == id).first()

    if inventory is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Inventory not found')

    category = Category.select().where(Category.id == inventory_request.fk_category.id).first()
    
    if category is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Category not found')

    inventory.product = inventory_request.product
    inventory.sku = inventory_request.sku
    inventory.ubication = inventory_request.ubication
    inventory.method = inventory_request.method
    inventory.date = formatted_date
    inventory.detail = inventory_request.detail
    inventory.amount = inventory_request.amount
    inventory.unit_value = inventory_request.unit_value
    inventory.fk_category = inventory_request.fk_category.id
    inventory.fk_user = user.id
    inventory.active = inventory_request.active

    inventory.save()

    return inventory


@router.delete('/{id}', response_model = InventoryResponseModel)
async def update_inventory(id: int, inventory_request: InventoryRequestPutModel, current_user: Users = Depends(get_current_user)):
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=3)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al inventario")


    inventory =  Inventory.select().where(Inventory.id == id).first()

    if inventory_request is None:
        raise HTTPException(status_code = 404, detail = 'Inventory no found')
    
    inventory.active = inventory_request.active = 1

    inventory.save()

    return inventory