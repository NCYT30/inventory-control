from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from datetime import datetime

from ..schemas import InventoryResponseModel
from ..schemas import InventoryRequestModel
from ..schemas import InventoryRequestPutModel

from ..database import Inventory

router = APIRouter(prefix = '/inventory')

@router.get('/', response_model = list[InventoryResponseModel])
async def get_inventory(page: int = 1, limit: int = 10):
    inventory = Inventory.select().where(Inventory.active == 0)

    return [ inv for inv in inventory]


@router.get('/{inventory_id}', response_model = InventoryResponseModel)
async def get_inventory_id(inventory_id: int = Path(..., title = 'Inventory  ID', ge = 1)):
    inventory = Inventory.get_or_none((Inventory.id == inventory_id) & (Inventory.active == 0))

    if inventory is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Inventory not found")
    
    return inventory


@router.post('/', response_model = InventoryResponseModel)
async def create_inventory(inventory: InventoryRequestModel):
    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_value = inventory.amount * inventory.unit_value

    inventory = Inventory.create(
        product = inventory.product,
        sku = inventory.sku,
        ubication = inventory.ubication,
        method = inventory.method,
        date = formatted_date,
        detail = inventory.detail,
        amount = inventory.amount,
        unit_value = inventory.unit_value,
        total_value = total_value,
        active = 0
    )

    return inventory

@router.put('/{id}', response_model = InventoryResponseModel)
async def update_inventory(id: int, inventory_request: InventoryRequestPutModel):

    inventory =  Inventory.select().where(Inventory.id == id).first()

    if inventory_request is None:
        raise HTTPException(status_code = 404, detail = 'Inventory no found')
    
    inventory.product = inventory_request.product
    inventory.sku = inventory_request.sku
    inventory.ubication = inventory_request.ubication
    inventory.method = inventory_request.method
    inventory.date = inventory_request.date
    inventory.detail = inventory_request.detail
    inventory.amount = inventory_request.amount
    inventory.unit_value = inventory_request.unit_value
    inventory.total_value = inventory_request.total_value
    inventory.active = 0

    inventory.save()

    return inventory




@router.delete('/{id}', response_model = InventoryResponseModel)
async def update_inventory(id: int, inventory_request: InventoryRequestPutModel):

    inventory =  Inventory.select().where(Inventory.id == id).first()

    if inventory_request is None:
        raise HTTPException(status_code = 404, detail = 'Inventory no found')
    
    inventory.active = inventory_request.active = 1

    inventory.save()

    return inventory

