from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShowCreate(BaseModel):
    movie_id: int
    start_time: datetime
    hall: str
    total_seats: int = 50


class ShowUpdate(BaseModel):
    start_time: Optional[datetime] = None
    hall: Optional[str] = None
    total_seats: Optional[int] = None


class ShowOut(BaseModel):
    id: int
    movie_id: int
    start_time: datetime
    hall: str
    total_seats: int

    model_config = {"from_attributes": True}
