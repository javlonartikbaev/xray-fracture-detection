from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.exc import IntegrityError
from apps.doctors.schemas import DoctorCreate, DoctorRead
from apps.doctors.services import create_doctor_service, get_doctors_service, get_doctor_service
from apps.registration.schemas import UserRead
from settings.db import get_db

router = APIRouter(prefix='/doctors', tags=['Doctors'])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=DoctorRead)
async def register_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):

    try:
        doctor = await create_doctor_service(doctor, db)
    except Exception as e:
        error = str(e.orig)
        if "phone_number" in error:
            detail = "Phone number already exists"
        raise HTTPException(status_code=400, detail=detail)
    return doctor



# Пока что не нужно
@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[DoctorRead])
async def list_doctors(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    result = await get_doctors_service(db, skip, limit)
    return result


@router.get('/{doctor_id}', status_code=status.HTTP_200_OK, response_model=DoctorRead)
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        doctor = await get_doctor_service(db, doctor_id)
    except:
        raise HTTPException(status_code=404, detail='Doctor not found')
    return doctor