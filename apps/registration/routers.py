from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from apps import User
from apps.registration.schemas import UserRead, UserCreate
from apps.registration.services import create_user, get_users
from settings.db import get_db

router = APIRouter(prefix='/users', tags=['Registration'])


@router.post('/register', response_model=UserCreate)
async def user_register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(user, db)
    except:
        raise HTTPException(status_code=400, detail="User already exists")
    return new_user


@router.get('/list', response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    return users
