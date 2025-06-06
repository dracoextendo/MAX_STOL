from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.utils.config import db_config

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

engine = create_async_engine(db_config.DATABASE_URL, connect_args={"ssl": None},)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

