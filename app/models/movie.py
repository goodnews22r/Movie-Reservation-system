from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(String, default="")

    shows = relationship("Show", back_populates="movie", cascade="all, delete-orphan")
