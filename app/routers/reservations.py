from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.session import get_db
from app.models.reservation import Reservation
from app.models.seat import Seat
from app.models.show import Show
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def _build_reservation_out(r: Reservation) -> ReservationOut:
    return ReservationOut(
        id=r.id,
        seat_id=r.seat_id,
        user_id=r.user_id,
        created_at=r.created_at,
        seat_number=r.seat.seat_number,
        show_id=r.seat.show_id,
        movie_title=r.seat.show.movie.title,
    )


@router.post("/", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def create_reservation(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reserve a seat for the current user."""
    seat = (
        db.query(Seat)
        .options(joinedload(Seat.show).joinedload(Show.movie))
        .filter(Seat.id == payload.seat_id)
        .first()
    )
    if not seat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found")

    if seat.is_reserved:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat is already reserved",
        )

    # Mark seat as reserved
    seat.is_reserved = True

    reservation = Reservation(user_id=current_user.id, seat_id=seat.id)
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    # Reload with relationships
    reservation = (
        db.query(Reservation)
        .options(
            joinedload(Reservation.seat)
            .joinedload(Seat.show)
            .joinedload(Show.movie)
        )
        .filter(Reservation.id == reservation.id)
        .first()
    )
    return _build_reservation_out(reservation)


@router.get("/my", response_model=List[ReservationOut])
def my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all reservations for the current user."""
    reservations = (
        db.query(Reservation)
        .options(
            joinedload(Reservation.seat)
            .joinedload(Seat.show)
            .joinedload(Show.movie)
        )
        .filter(Reservation.user_id == current_user.id)
        .all()
    )
    return [_build_reservation_out(r) for r in reservations]


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancel a reservation and free up the seat."""
    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id, Reservation.user_id == current_user.id)
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or does not belong to you",
        )

    # Free the seat
    seat = db.query(Seat).filter(Seat.id == reservation.seat_id).first()
    if seat:
        seat.is_reserved = False

    db.delete(reservation)
    db.commit()
