from passlib.context import CryptContext
from settings.conf import settings
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.doctors.models import Doctor
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends
from settings.db import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_doctor_by_phone_number(phone_number: str, db: AsyncSession):
    result = await db.execute(select(Doctor).
                        where(Doctor.phone_number == phone_number))
    
    doctor = result.scalar_one_or_none()
    return doctor

async def get_current_user(credentials = Security(security), 
                           db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    doctor_id = int(payload.get("doctor_id"))
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return doctor

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    print("to_encode", to_encode)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("encoded_jwt", encoded_jwt)
    return encoded_jwt