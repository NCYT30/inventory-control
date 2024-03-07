from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, status, Depends

from ..schemas import SalesResponseModel
from ..schemas import SalesRequestModel
from ..schemas import SalesRequestPutModel

from ..database import Sales
from ..database import Inventory
from ..database import RolPer, Users

from .login import get_current_user




router = APIRouter(prefix = '/sales')

@router.get('/', response_model = list[SalesResponseModel])
async def get_sales(page: int = 1, limit: int = 10, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=6)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a ventas")

    sales = Sales.select()

    return [ sale for sale in sales ]


@router.post('/', response_model = SalesResponseModel)
async def create_sales(sales: SalesRequestModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=6)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a ventas")


    try:
        inventory = Inventory.get(Inventory.id == sales.fk_inv.id)
    except Inventory.DoesNotExist:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Inventory not found')

    if sales.amount > inventory.amount:
        raise HTTPException(status_code = 400, detail = 'Insufficient stock')

    total = sales.amount * inventory.unit_value

    sales = Sales.create(
        fk_inv = sales.fk_inv.id,
        amount = sales.amount,
        total_value = total
    )

    inventory.amount -= sales.amount
    inventory.save()

    return sales



@router.put('/{id}', response_model = SalesResponseModel)
async def update_sales(id: int, sales_request: SalesRequestPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=6)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a ventas")


    sales = Sales.select().where(Sales.id == id).first()

    inventory = Inventory.select().where(Inventory.id == sales_request.fk_inv.id).first()

    if sales is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Sales not found')

    if inventory is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Inventory not found')

    inventory = None

    amount_change = sales_request.amount - sales.amount

    if amount_change != 0:

        inventory = Inventory.get(Inventory.id == sales.fk_inv)

        if inventory is None:
            raise HTTPException(status_code = 404, detail = "Inventory not found")

        if amount_change > inventory.amount:
            raise HTTPException(status_code=400, detail="Insufficient stock to update sale")
        
        inventory.amount -= amount_change
        inventory.save()
    
    total_value = sales_request.amount * inventory.unit_value if inventory else 0

    sales.amount = sales_request.amount
    sales.total_value = total_value

    sales.save()

    return sales