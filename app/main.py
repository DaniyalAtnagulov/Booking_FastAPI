import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date
import time
from typing import Annotated, Optional

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from fastapi_versioning import VersionedFastAPI

from app import logger
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.model import Users
from app.users.router import (
    router as router_users,  # ,router_auth доработка функционала 1.8
)

app = FastAPI()

# import logging       

async def get_data():
    data = await asyncio.sleep(3) # имитация данных необходимых для старта приложения 
    
async def get_cache():
    while True:
        await get_data()
        await asyncio.sleep(60*5)  # имитация кода, наполняющего справочные данные или набирание кэша, бесконечная функция 

# при запуске 
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}") 
    FastAPICache.init(RedisBackend(redis), prefix="cache") #prefix="fastapi-cache" изначально
    # await get_data()
    # asyncio.create_task(get_cache()) # бесконечная задача
    yield
# при выключении (на данный моент этот кусок кода еще не написан)

app = FastAPI(lifespan=lifespan)  # lifespan также нужно будет передатьь в VersionedFastAPI

'''Ниже закомментирован более новый способ  '''

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
    
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Service started")
#     yield
#     logger.info("Service exited")

#app = FastAPI(lifespan=lifespan)




#app.include_router(router_auth)                          доработка функционала
app.include_router(router_users)
app.include_router(router_hotels)        
app.include_router(router_bookings)

app.include_router(router_pages)

app.include_router(router_images)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type", 
        "Set-Cookie", 
        "Access-Control-Allow-Headers", 
        "Access-Control-Allow-Origin", 
        "Authorization"
    ],
)




# class SHotel(BaseModel):
#     adress: str
#     name: str
#     stars: int
    

@app.get('/hotels') #,response_model=list[SHotel])
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Annotated[bool | None, Query()] = None,         
    stars: Annotated[int | None, Query(ge=1,le=5)] = None 
):
    hotels = [
            {
                'adress': 'Altai',
                'name': 'SuperHotel',
                "stars": 5,
               }
              ]
    return hotels




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        "Request handling time",
        extra={"process_time": round(process_time, 4)}
    )

    return response

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
#     description='Greet users with a nice message',
#     middleware=[
#         Middleware(SessionMiddleware, secret_key='mysecretkey')
#     ]
 )

app.mount("/static", StaticFiles(directory="app/static"), "static")  # static-файлы лучше монтировать после VersionedFastAPI, т.е. конкретно к эиому приложению

admin = Admin(    ## админки также могут использовать static-файлы, но под капотом                                           
    app=app,
    engine=engine,
    authentication_backend=authentication_backend)  


    
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)



# class SBooking(BaseModel):
#     room_id: int
#     date_from: date
#     date_to: date

# @app.post('/bookings')
# def add_booking(booking: SBooking):
#     pass

# С версии 0.95.0 рекомендуется использовать именно Annotated. Вот пример: 
# stars: Annotated[int | None, Query(ge=1, le=5)] = None
# К сожалению Swagger UI не поддерживает int | None в таком случае, 
# и мы будем видеть просто что это query param (без типа integer, minimum и maximum). 
# Это проблема именно Swagger UI (он просто не поддерживает эту фичу OpenAPI спецификации), но зато ReDoc поддерживает. 
# Так что рекомендую смотреть именно на ReDoc (на самом деле крутой инструмент, 
# просто в отличии от Swagger UI он не позволяет отправлять запросы).



# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Привет, мир"}
