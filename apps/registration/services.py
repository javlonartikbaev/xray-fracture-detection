from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .models import User
from datetime import date

from .schemas import UserCreate


async def create_user(user: UserCreate, db: AsyncSession) -> User:
    user = User(
        **user.model_dump()
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users