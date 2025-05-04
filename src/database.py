from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

database_url = 'sqlite+aiosqlite:///../database.db'
alembic_db_url = 'sqlite+aiosqlite:///database.db'
engine = create_async_engine(database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

