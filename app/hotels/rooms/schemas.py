from datetime import date

from pydantic import BaseModel, ConfigDict

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int 
    
    model_config = ConfigDict(from_attributes=True)
    
    # class Config():
    #     orm_mode = True    старый метод  
    
class SAvaibleRoom(BaseModel):
    id : int 
    hotel_id : int 
    name : str 
    description : str 
    services : list[str] 
    price : int 
    quantity : str 
    image_id : int 
    total_cost : int
    rooms_left : int
    
    
