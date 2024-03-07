from fastapi import FastAPI
from fastapi import APIRouter

from .database import Inventory
from .database import Users
from .database import Providers
from .database import Permissions
from .database import RolPer
from .database import Category
from .database import Sales

from .routers import inventory_router
from .routers import users_router
from .routers import providers_router
from .routers import category_router
from .routers import sales_router
from .routers import permissions_router
from .routers import rol_router
from .routers import login_router

from .database import database as connection


app = FastAPI()

api_v1 = APIRouter(prefix = '/api/v1')

api_v1.include_router(inventory_router)
api_v1.include_router(users_router)
api_v1.include_router(providers_router)
api_v1.include_router(category_router)
api_v1.include_router(sales_router)
api_v1.include_router(permissions_router)
api_v1.include_router(rol_router)
api_v1.include_router(login_router)

app.include_router(api_v1)

@app.on_event('startup')
def startup():
  if connection.is_closed():
      connection.connect()

  connection.create_tables([Inventory, Users, Providers, Permissions, RolPer, Category, Sales])


@app.on_event('shutdown')
def shutdown():
  if not connection.is_closed():
      connection.close()

