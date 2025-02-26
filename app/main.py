from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from typing import Annotated, Optional
from datetime import date


from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users #,router_auth доработка функционала 1.8
from app.hotels.router import router as router_hotels        
from app.pages.router import router as router_pages

from app.images.router import router as router_images

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

#app.include_router(router_auth)                          доработка функционала
app.include_router(router_users)
app.include_router(router_hotels)        
app.include_router(router_bookings)

app.include_router(router_pages)

app.include_router(router_images)


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
