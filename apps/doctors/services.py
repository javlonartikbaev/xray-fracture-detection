from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from datetime import date

from apps import Doctor
from .schemas import DoctorCreate


async def create_doctor(doctor: DoctorCreate, db: AsyncSession):  # create doctor
    doctor = Doctor(**doctor.model_dump())
    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor


async def get_doctors(db: AsyncSession, skip: int = 0, limit: int = 10):  # list  doctor
    result = await db.execute(select(Doctor).offset(skip).limit(limit))
    doctors = result.scalars().all()
    return doctors


async def get_doctor(db: AsyncSession, doctor_id: int):  # get 1 doctor
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    user = result.scalar_one_or_none()
    return user


async def delete_doctor(db: AsyncSession, doctor_id: int):  # delete doctor
    doctor = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    await db.delete(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor
