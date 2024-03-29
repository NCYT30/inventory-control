from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, Depends, status

from ..database import Providers, RolPer, Users

from ..schemas import ProvidersResponseModel
from ..schemas import ProvidersRequestModel
from ..schemas import ProvidersPutModel

from .login import get_current_user


router = APIRouter(prefix = '/providers')

@router.get('/', response_model = list[ProvidersResponseModel])
async def get_providers(page: int = 1, limit = 10, current_user: Users = Depends(get_current_user)):
   
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=4)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a proveedores")

    providers = Providers.select().where(Providers.active == 0)

    return [ provider for provider in providers]


@router.get('/{providers_id}', response_model = ProvidersResponseModel)
async def get_providers_id(providers_id: int = Path(..., title = 'Providers ID', ge = 1), current_user: Users = Depends(get_current_user)) :

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=4)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a proveedores")


    providers = Providers.get_or_none((Providers.id == providers_id) & (Providers.active == 0))

    if providers is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Providers not found")
    
    return providers



@router.post('/', response_model = ProvidersResponseModel)
async def create_providers(providers: ProvidersRequestModel, current_user: Users = Depends(get_current_user)):
    
    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=4)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a proveedores")


    providers = Providers.create(
        name = providers.name,
        description = providers.description,
        addres = providers.addres,
        email = providers.email,
        phone = providers.phone,
        fkusr_id = user.id,
        active = 0
    )

    return providers



@router.put('/{id}', response_model = ProvidersResponseModel)
async def update_providers(id: int, providers_request: ProvidersPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=4)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a proveedores")


    provider = Providers.select().where(Providers.id == id).first()

    if provider is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Providers not found')

    provider.name = providers_request.name
    provider.description = providers_request.description
    provider.addres = providers_request.addres
    provider.email = providers_request.email
    provider.phone = providers_request.phone

    provider.save()

    return provider


@router.delete('/{id}', response_model = ProvidersResponseModel)
async def delete_user(id: int, useproviders_requestrs_request: ProvidersPutModel, current_user: Users = Depends(get_current_user)):

    user = await current_user  
    permission = RolPer.get_or_none(fk_user=user.id, fk_per=4)
    if not permission:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a proveedores")


    provider = Providers.select().where(Providers.id == id).first()

    if provider is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Providers not found')


    provider.active = 1

    provider.save()

    return provider