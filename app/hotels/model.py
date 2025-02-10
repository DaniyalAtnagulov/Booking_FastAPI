from typing import Optional
from sqlalchemy import JSON, ForeignKey
from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped

class Hotels(Base):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False) 
    image_id: Mapped[int] 
    
    
class Rooms(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] 
    services: Mapped[Optional[list[str]]] = mapped_column(JSON) # Также обратите внимание, что параметр nullable теперь также отражен внутри подсказки типа: Optional говорит о том, что поле может быть пустым в базе данных, а его отсутствие -- что поле обязательно и не может быть пустым (NOT NULL)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]