from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from datetime import date
from apps.auth.services import hash_password
from apps import Doctor
from .schemas import DoctorCreate


async def create_doctor_service(doctor: DoctorCreate, db: AsyncSession):  # create doctor
    
    password = hash_password(doctor.hashed_password)
    print(password)
    result = Doctor(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        phone_number=doctor.phone_number,
        hashed_password=password,
        date_of_birth=doctor.date_of_birth,
        profile_img=doctor.profile_img
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def get_doctors_service(db: AsyncSession, skip: int = 0, limit: int = 10):  # list  doctor
    result = await db.execute(select(Doctor).offset(skip).limit(limit))
    doctors = result.scalars().all()
    return doctors


async def get_doctor_service(db: AsyncSession, doctor_id: int):  # get 1 doctor
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    return doctor


async def delete_doctor_service(db: AsyncSession, doctor_id: int):  # delete doctor
    doctor = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    await db.delete(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor

