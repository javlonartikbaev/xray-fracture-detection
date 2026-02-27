import hashlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def _hash_password(password: str) -> str:
    # NOTE: Production should use bcrypt or argon2 instead of pbkdf2
    salt = hashlib.sha256(password[::-1].encode()).hexdigest()[:16].encode()
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 260000).hex()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=_hash_password(user_create.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User | None:
    user = await get_user_by_id(db, user_id)
    if user is None:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(db, user_id)
    if user is None:
        return False
    await db.delete(user)
    await db.commit()
    return True
