

from pydantic import BaseModel, ConfigDict
from datetime import date

from apps.registration.models import UserGender


class LoginSchema(BaseModel):
    phone_number: str
    password: str
