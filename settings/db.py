from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from conf import settings

DB_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PW}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(DB_URL)
session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
DeclarativeBase = declarative_base()


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
