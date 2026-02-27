import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr, DeclarativeBase
from sqlalchemy import func




class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'
