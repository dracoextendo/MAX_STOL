from sqlalchemy import select
from typing import override

from src.models.users import UsersModel
from src.utils.database import async_session_maker
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

    @override
    async def get_one_by_username(self, username: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()