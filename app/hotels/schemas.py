from datetime import date

from pydantic import BaseModel

class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    
    # class Config():
    #     orm_mode = True  
    
class SHotelInfo(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int