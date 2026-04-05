from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(String, nullable=False)
    is_reserved = Column(Boolean, default=False, nullable=False)

    show = relationship("Show", back_populates="seats")
    reservation = relationship("Reservation", back_populates="seat", uselist=False)
