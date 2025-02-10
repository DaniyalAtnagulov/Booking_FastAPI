from datetime import date
#чтобы не прописывать заново атрибуты класса SBooking, беря их из Bokkings можно использовать SQLModel
from pydantic import BaseModel

class SBooking(BaseModel):
    id: int             
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    
    
    # class Config():
    #     orm_mode = True    