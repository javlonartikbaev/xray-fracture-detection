from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from apps.doctors.schemas import DoctorCreate, DoctorRead
from apps.doctors.services import create_doctor, get_doctors
from apps.registration.schemas import UserRead
from settings.db import get_db

router = APIRouter(prefix='/doctors', tags=['Doctors'])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=DoctorRead)
async def register_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    doctor = await create_doctor(doctor, db)
    return doctor


@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[DoctorRead])
async def list_doctors(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    result = await get_doctors(db, skip, limit)
    return result
