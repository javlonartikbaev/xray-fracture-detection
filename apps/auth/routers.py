from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends
from apps.auth.schemas import LoginSchema
from apps.auth.services import create_access_token, get_doctor_by_phone_number, verify_password
from settings.db import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    doctor = await get_doctor_by_phone_number(data.phone_number, db)
    if not doctor:
        raise HTTPException(status_code=400, 
                            detail="Doctor with this phone number does not exist")
    
    if not verify_password(data.password, doctor.hashed_password):
        raise HTTPException(status_code=400, 
                            detail="Invalid phone number or password")
    

    access_token = create_access_token(data={"sub": doctor.phone_number,
                                              "doctor_id": doctor.id})

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}