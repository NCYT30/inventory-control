from fastapi import FastAPI
from fastapi import APIRouter

from .database import Inventory
from .database import Users
from .database import Providers

from .routers import inventory_router
from .routers import users_router
from .routers import providers_router

from .database import database as connection


app = FastAPI()

api_v1 = APIRouter(prefix = '/api/v1')

api_v1.include_router(inventory_router)
api_v1.include_router(users_router)
api_v1.include_router(providers_router)

app.include_router(api_v1)

@app.on_event('startup')
def startup():
  if connection.is_closed():
      connection.connect()

  connection.create_tables([Inventory, Users, Providers])


@app.on_event('shutdown')
def shutdown():
  if not connection.is_closed():
      connection.close()

