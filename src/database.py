from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.config import DBConfig

dbconfig = DBConfig()

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

database_url = f"postgresql+asyncpg://{dbconfig.user.get_secret_value()}:{dbconfig.password.get_secret_value()}@{dbconfig.host.get_secret_value()}:{dbconfig.port.get_secret_value()}/{dbconfig.name.get_secret_value()}"
engine = create_async_engine(database_url, connect_args={"ssl": None},)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

