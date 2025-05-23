from sqlalchemy.future import select
from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model).order_by(cls.model.sort, cls.model.id)
            result = await session.execute(query)
            return result.scalars().all()
