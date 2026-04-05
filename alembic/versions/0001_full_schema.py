"""Full schema: users, movies, shows, seats, reservations

Revision ID: 0001_full_schema
Revises:
Create Date: 2026-01-27 00:00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_full_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("genre", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_movies_id", "movies", ["id"], unique=False)

    op.create_table(
        "shows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("hall", sa.String(), nullable=False),
        sa.Column("total_seats", sa.Integer(), nullable=False, server_default="50"),
        sa.ForeignKeyConstraint(["movie_id"], ["movies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_shows_id", "shows", ["id"], unique=False)

    op.create_table(
        "seats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("show_id", sa.Integer(), nullable=False),
        sa.Column("seat_number", sa.String(), nullable=False),
        sa.Column("is_reserved", sa.Boolean(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["show_id"], ["shows.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_seats_id", "seats", ["id"], unique=False)

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("seat_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["seat_id"], ["seats.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("seat_id"),
    )
    op.create_index("ix_reservations_id", "reservations", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("reservations")
    op.drop_table("seats")
    op.drop_table("shows")
    op.drop_table("movies")
    op.drop_table("users")
