from pydantic import BaseModel, ConfigDict
from datetime import date

from apps.registration.models import UserGender


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    hashed_password: str
    date_of_birth: date
    profile_img: str


class DoctorRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    date_of_birth: date
    profile_img: str
    model_config = ConfigDict(from_attributes=True)
