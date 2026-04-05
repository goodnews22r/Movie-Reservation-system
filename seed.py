"""
Seed script – run once to populate the database with sample data.

    python seed.py

Creates:
  • admin@example.com  / admin123   (is_admin=True)
  • user@example.com   / user123    (is_admin=False)
  • 3 movies, 2 shows each, seats auto-generated
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.movie import Movie
from app.models.show import Show
from app.models.seat import Seat
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_users():
    if db.query(User).first():
        print("Users already seeded, skipping.")
        return
    users = [
        User(email="admin@example.com", hashed_password=hash_password("admin123"), is_admin=True),
        User(email="user@example.com", hashed_password=hash_password("user123"), is_admin=False),
    ]
    db.add_all(users)
    db.commit()
    print("✓ Users seeded")


def seed_movies_and_shows():
    if db.query(Movie).first():
        print("Movies already seeded, skipping.")
        return

    movies_data = [
        {"title": "Inception", "description": "A thief who steals corporate secrets through dream-sharing technology.", "duration_minutes": 148, "genre": "Sci-Fi"},
        {"title": "The Dark Knight", "description": "Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos.", "duration_minutes": 152, "genre": "Action"},
        {"title": "Interstellar", "description": "A team of explorers travel through a wormhole in space.", "duration_minutes": 169, "genre": "Sci-Fi"},
    ]

    now = datetime.utcnow()
    for movie_data in movies_data:
        movie = Movie(**movie_data)
        db.add(movie)
        db.flush()

        for i in range(2):
            show = Show(
                movie_id=movie.id,
                start_time=now + timedelta(days=i + 1, hours=18),
                hall=f"Hall {i + 1}",
                total_seats=30,
            )
            db.add(show)
            db.flush()

            # Generate seats A1-A10, B1-B10, C1-C10
            seats = []
            for row in "ABC":
                for num in range(1, 11):
                    seats.append(Seat(show_id=show.id, seat_number=f"{row}{num}"))
            db.add_all(seats)

    db.commit()
    print("✓ Movies, shows, and seats seeded")


if __name__ == "__main__":
    seed_users()
    seed_movies_and_shows()
    db.close()
    print("\nDatabase seeded successfully!")
    print("  Admin login: admin@example.com / admin123")
    print("  User login:  user@example.com  / user123")
