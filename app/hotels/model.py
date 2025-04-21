from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.hotels.rooms.model import Rooms

class Hotels(Base):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False) 
    image_id: Mapped[int] 
    
    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self) -> str:
        return self.name