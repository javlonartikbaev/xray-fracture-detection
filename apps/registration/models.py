from datetime import date
import enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Enum

from settings.base import Base


class UserGender(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(Base):
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(16), unique=True)
    passport_number: Mapped[str] = mapped_column(String(8), unique=True)
    passport_pinfl: Mapped[str] = mapped_column(String(14), unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date())
    gender: Mapped[UserGender] = mapped_column(Enum(UserGender))
