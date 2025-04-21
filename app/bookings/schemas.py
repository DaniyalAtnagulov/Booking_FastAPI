from datetime import date
from typing import Optional

#чтобы не прописывать заново атрибуты класса SBooking, беря их из Bokkings можно использовать SQLModel
from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    id: int             
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    
        # новый способ
    model_config = ConfigDict(from_attributes=True)
    
    
    #старый спсособ
    # class Config():
    #     orm_mode = True 
    
class SBookingInfo(BaseModel):
    Image_id: int
    name: str
    description: Optional[str]
    services: list[str]
       
class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    
class SBookingWithRoomInfo(BaseModel):
    room_id: int 
    user_id: int
    date_from: date 
    date_to: date
    price: int 
    total_cost: int 
    total_days: int 
    image_id: int 
    name: str 
    description: str 
    services: list[str]  