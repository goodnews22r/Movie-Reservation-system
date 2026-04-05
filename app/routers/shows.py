from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.show import Show
from app.models.seat import Seat
from app.models.movie import Movie
from app.models.user import User
from app.schemas.show import ShowCreate, ShowUpdate, ShowOut
from app.schemas.seat import SeatOut
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/shows", tags=["Shows"])


def _generate_seats(db: Session, show: Show):
    """Auto-generate seat rows A–E with seat numbers for a new show."""
    rows = "ABCDEFGHIJ"
    seats_per_row = max(1, show.total_seats // 10)
    seats = []
    count = 0
    for row in rows:
        for num in range(1, seats_per_row + 1):
            if count >= show.total_seats:
                break
            seats.append(Seat(show_id=show.id, seat_number=f"{row}{num}"))
            count += 1
        if count >= show.total_seats:
            break
    db.add_all(seats)
    db.commit()


@router.get("/", response_model=List[ShowOut])
def list_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()


@router.get("/{show_id}", response_model=ShowOut)
def get_show(show_id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show


@router.post("/", response_model=ShowOut, status_code=status.HTTP_201_CREATED)
def create_show(
    payload: ShowCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: create a show for a movie and auto-generate seats."""
    movie = db.query(Movie).filter(Movie.id == payload.movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    show = Show(**payload.model_dump())
    db.add(show)
    db.commit()
    db.refresh(show)

    _generate_seats(db, show)
    return show


@router.put("/{show_id}", response_model=ShowOut)
def update_show(
    show_id: int,
    payload: ShowUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: update show scheduling info."""
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(show, field, value)

    db.commit()
    db.refresh(show)
    return show


@router.delete("/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_show(
    show_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: delete a show and its seats."""
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    db.delete(show)
    db.commit()


@router.get("/{show_id}/seats", response_model=List[SeatOut])
def get_seats(show_id: int, db: Session = Depends(get_db)):
    """List all seats for a show with real availability status."""
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    seats = db.query(Seat).filter(Seat.show_id == show_id).all()
    return seats
