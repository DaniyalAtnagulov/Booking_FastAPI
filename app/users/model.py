from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.bookings.model import Bookings

class Users(Base):
    __tablename__= 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable= False)
    
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return self.email