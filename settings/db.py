from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import sessionmaker, Session, declarative_base
from settings.conf import settings

DB_URL_ASYNC = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
DB_URL_SYNC = f'postgresql://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
print("FASTAPI DB:", DB_URL_ASYNC)

engine = create_async_engine(DB_URL_ASYNC)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)



async def get_db():
    async with session_factory() as db:
        yield db



db_dependency = Annotated[AsyncSession, Depends(get_db)]
