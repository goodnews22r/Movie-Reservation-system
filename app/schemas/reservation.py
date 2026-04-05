from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    seat_id: int


class ReservationOut(BaseModel):
    id: int
    seat_id: int
    user_id: int
    created_at: datetime
    seat_number: str
    show_id: int
    movie_title: str

    model_config = {"from_attributes": True}
