"""
Service layer for reservation business logic.
Kept separate so routers stay thin and logic can be tested independently.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.reservation import Reservation
from app.models.seat import Seat


def reserve_seat(db: Session, user_id: int, seat_id: int) -> Reservation:
    seat = db.query(Seat).filter(Seat.id == seat_id).with_for_update().first()

    if not seat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found")

    if seat.is_reserved:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat is already reserved",
        )

    seat.is_reserved = True
    reservation = Reservation(user_id=user_id, seat_id=seat_id)
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def cancel_reservation(db: Session, reservation_id: int, user_id: int) -> None:
    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id, Reservation.user_id == user_id)
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    seat = db.query(Seat).filter(Seat.id == reservation.seat_id).first()
    if seat:
        seat.is_reserved = False

    db.delete(reservation)
    db.commit()
