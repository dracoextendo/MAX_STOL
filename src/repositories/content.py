from typing import override

from sqlalchemy import select

from src.models.content import ContentModel
from src.utils.repository import SQLAlchemyRepository


class ContentRepository(SQLAlchemyRepository):
    model = ContentModel

    @override
    async def get_first(self):
        async with self.session_factory() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().first()