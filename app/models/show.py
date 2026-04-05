from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    hall = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False, default=50)

    movie = relationship("Movie", back_populates="shows")
    seats = relationship("Seat", back_populates="show", cascade="all, delete-orphan")
