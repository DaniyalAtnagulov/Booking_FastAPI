from datetime import date

from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    
        # новый способ
    model_config = ConfigDict(from_attributes=True)
    
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