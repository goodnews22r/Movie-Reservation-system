from fastapi import FastAPI
from app.routers import auth, movies, shows, reservations
from app.db.session import engine
from app.db.base import Base

# Create all tables on startup (dev convenience; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Reservation System",
    description="Book seats for movie screenings. Admins manage movies & shows.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(shows.router)
app.include_router(reservations.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Movie Reservation System is running"}
