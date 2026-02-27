from pydantic import BaseModel, ConfigDict
from datetime import date

from apps.registration.models import UserGender


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    passport_number: str
    passport_pinfl: str
    date_of_birth: date
    gender: UserGender


class UserRead(UserCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
