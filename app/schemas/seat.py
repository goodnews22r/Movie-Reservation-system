from pydantic import BaseModel


class SeatOut(BaseModel):
    id: int
    seat_number: str
    is_reserved: bool

    model_config = {"from_attributes": True}
