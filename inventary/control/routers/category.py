from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, status, Depends

from ..schemas import CategoryResponseModel
from ..schemas import CategoryRequestModel
from ..schemas import CategoryPutModel


from ..database import Category, RolPer, Users

from .login import get_current_user


router = APIRouter(prefix = '/category')


@router.get('/', response_model = list[CategoryResponseModel])
async def get_category(page: int = 1, limit: int = 10, current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=5)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a categoria")


    category = Category.select()

    return [ categor for categor in category]

@router.get('/{id_cate}', response_model = CategoryResponseModel)
async def get_category_id(id_cate: int = Path(..., title = 'Category ID', ge = 1), current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=5)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a categoria")


    category = Category.get_or_none((Category.id == id_cate))

    if category is None:
        raise HTTPException(status_code  = status.HTTP_404_NOT_FOUND, detail = "Category not found")
    
    return category

@router.post('/', response_model = CategoryResponseModel)
async def create_category(category: CategoryRequestModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=5)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a categoria")


    cate = Category.create(
        name = category.name
    )

    return cate

@router.put('/{id}', response_model = CategoryResponseModel)
async def update_category(id: int, category_request: CategoryPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=5)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a categoria")


    category = Category.select().where(Category.id == id).first()

    if category is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Category not found')

    category.name = category_request.name

    category.save()

    return category


@router.delete('/{id}', response_model = CategoryResponseModel)
async def delete_category(id: int,  current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=5)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a categoria")

    category = Category.select().where(Category.id == id).first()

    if category is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Category not found')

    category.delete_instance()

    return category