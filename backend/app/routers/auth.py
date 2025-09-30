# backend/app/db_models.py
from sqlalchemy import String, Date, DateTime, UniqueConstraint, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from backend.app.database import Base


# -----------------------------
# Usuário
# -----------------------------
class User(Base):
    _tablename_ = "users"
    _table_args_ = (
        UniqueConstraint("name", name="uq_users_name"),
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("phone", name="uq_users_phone"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)