from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date

from settings.base import Base


class Doctor(Base):
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(16))
    hashed_password: Mapped[str] = mapped_column(String())
    date_of_birth: Mapped[date] = mapped_column(Date())
    profile_img: Mapped[str | None] = mapped_column(String(255), nullable=True)
