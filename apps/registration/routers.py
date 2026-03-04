from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps import User
from apps.auth.services import get_current_user
from apps.doctors.models import Doctor
from apps.registration.schemas import UserRead, UserCreate
from apps.registration.services import create_user, get_users
from settings.db import get_db
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/users', tags=['Registration'])


@router.post('/register', response_model=UserCreate)
async def user_register(user: UserCreate, db: AsyncSession = Depends(get_db), _: Doctor = Depends(get_current_user)):
    try:
        new_user = await create_user(user, db)
    except IntegrityError as e:
        error = str(e.orig)

        if "phone_number" in error:
            detail = "Phone number already exists"
        elif "passport_number" in error:
            detail = "Passport number already exists"
        elif "passport_pinfl" in error:
            detail = "PINFL already exists"
        else:
            detail = "User already exists"

        raise HTTPException(status_code=400, detail=detail)
    return new_user


@router.get('/list', response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db), 
                     _: Doctor = Depends(get_current_user)):
    users = await get_users(db)
    return users
