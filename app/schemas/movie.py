from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    duration_minutes: int
    genre: Optional[str] = ""


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None


class ShowOut(BaseModel):
    id: int
    start_time: datetime
    hall: str
    total_seats: int

    model_config = {"from_attributes": True}


class MovieOut(BaseModel):
    id: int
    title: str
    description: str
    duration_minutes: int
    genre: str
    shows: List[ShowOut] = []

    model_config = {"from_attributes": True}
