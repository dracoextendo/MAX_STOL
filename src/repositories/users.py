from sqlalchemy import select
from typing import override
from src.models.users import UsersModel
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

    @override
    async def get_one_by_username(self, username: str):
        async with self.session_factory() as session:
            stmt = select(self.model).where(self.model.username == username)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            if not res:
                return None
            return res.to_read_password_model()