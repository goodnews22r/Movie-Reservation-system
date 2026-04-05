# 🎬 Movie Reservation System

A FastAPI-based REST API for browsing movies, scheduling shows, and booking seats.

---

## Features

| Feature | Details |
|---|---|
| Auth | JWT-based register/login, admin role |
| Movies | CRUD (admin), public listing |
| Shows | CRUD (admin), auto seat generation |
| Seats | Per-show availability listing |
| Reservations | Book a seat, view bookings, cancel |

---

## Project Structure

```
Movie Reservation System/
├── app/
│   ├── core/
│   │   ├── config.py          # Env vars (DATABASE_URL, SECRET_KEY, etc.)
│   │   └── security.py        # Password hashing, JWT encode/decode
│   ├── db/
│   │   ├── base.py            # SQLAlchemy Base + all model imports
│   │   └── session.py         # Engine, SessionLocal, get_db()
│   ├── models/
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── show.py
│   │   ├── seat.py
│   │   └── reservation.py     # ← NEW
│   ├── schemas/
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── show.py            # ← was empty, now complete
│   │   ├── seat.py
│   │   └── reservation.py     # ← NEW
│   ├── routers/
│   │   ├── auth.py            # /auth/register, /auth/login, /auth/me
│   │   ├── movies.py          # /movies CRUD
│   │   ├── shows.py           # /shows CRUD + /shows/{id}/seats
│   │   └── reservations.py    # /reservations — book, list, cancel ← NEW
│   ├── services/
│   │   └── reservation_service.py
│   ├── utils/
│   │   └── auth.py            # get_current_user, get_current_admin
│   └── main.py
├── alembic/
│   └── versions/
│       └── 0001_full_schema.py
├── seed.py                    # Populate DB with sample data
├── .env
├── alembic.ini
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Edit `.env` (already provided with sensible defaults):

```env
DATABASE_URL=sqlite:///./movie.db
SECRET_KEY=supersecretkey_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run migrations (or let the app auto-create tables)

```bash
alembic upgrade head
```

### 4. Seed sample data

```bash
python seed.py
```

This creates:
- **Admin**: `admin@example.com` / `admin123`
- **User**: `user@example.com` / `user123`
- 3 movies, 2 shows each, 30 seats per show

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Overview

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | — | Register new user |
| POST | `/auth/login` | — | Login, get JWT |
| GET | `/auth/me` | ✅ User | Get current user profile |

### Movies

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/movies/` | — | List all movies |
| GET | `/movies/{id}` | — | Get movie details |
| POST | `/movies/` | 🔑 Admin | Create movie |
| PUT | `/movies/{id}` | 🔑 Admin | Update movie |
| DELETE | `/movies/{id}` | 🔑 Admin | Delete movie |

### Shows

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/shows/` | — | List all shows |
| GET | `/shows/{id}` | — | Get show details |
| POST | `/shows/` | 🔑 Admin | Create show (seats auto-generated) |
| PUT | `/shows/{id}` | 🔑 Admin | Update show |
| DELETE | `/shows/{id}` | 🔑 Admin | Delete show |
| GET | `/shows/{id}/seats` | — | List seats with availability |

### Reservations

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/reservations/` | ✅ User | Book a seat |
| GET | `/reservations/my` | ✅ User | List my reservations |
| DELETE | `/reservations/{id}` | ✅ User | Cancel a reservation |

---

## Bugs Fixed from Original Code

1. **Dead code after `return`** in `core/security.py` — unreachable lines removed
2. **`status` not imported** in `routers/auth.py` — caused `NameError` on login
3. **Duplicate router registration** in `main.py` — both `app.auth.router` and `app.routers.auth` were mounted at `/auth`
4. **`settings` object undefined** in `utils/auth.py` — config used plain variables, not a settings object
5. **Two separate `Base` instances** — `models/user.py` imported from `app.database`, others from `app.db.base`; unified to single Base
6. **Duplicate `Token` schema** in `schemas/user.py` — second definition silently overwrote first
7. **Hard-coded DB URL** in `db/session.py` — ignored `.env` entirely
8. **`is_available` was always `True`** in shows router — seat model had no boolean field; fixed with real `is_reserved` column
9. **`schemas/show.py` was empty** — no schemas defined despite being used
10. **Migration `d2e806872cea` was a stub** — `upgrade()` just had `pass`; replaced with full schema migration
