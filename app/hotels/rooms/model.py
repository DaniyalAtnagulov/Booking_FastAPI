from typing import TYPE_CHECKING, Optional
from sqlalchemy import JSON, ForeignKey
from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from app.bookings.model import Bookings
    from app.hotels.model import Hotels

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
    
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")
    
    """Правило:
    Если связь многие-к-одному или один-к-одному, то просто "ModelName".
    Если связь один-ко-многим, то list["ModelName"]."""
    
    def __str__(self):
        return f"Номер {self.name}"