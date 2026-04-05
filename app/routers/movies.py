from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.session import get_db
from app.models.movie import Movie
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieUpdate, MovieOut
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=List[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    """List all movies with their scheduled shows."""
    return db.query(Movie).options(joinedload(Movie.shows)).all()


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).options(joinedload(Movie.shows)).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@router.post("/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(
    payload: MovieCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: create a new movie."""
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: update movie details."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Admin only: delete a movie and its shows/seats."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(movie)
    db.commit()
