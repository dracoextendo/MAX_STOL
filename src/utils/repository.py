from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.utils.database import async_session_maker


class AbstractRepository(ABC):

    @abstractmethod
    async def get_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def update_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_first(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_info(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_one_by_username(self):
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = async_session_maker):
        self.session_factory = session_factory

    async def get_one(self, id: int):
        async with self.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            if not res:
                return None
            return res.to_read_model()

    async def add_one(self, data: dict) -> int:
        async with self.session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, id: int, data: dict) -> int | None:
        async with self.session_factory() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def delete_one(self, id: int) -> int | None:
        async with self.session_factory() as session:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_all(self, filter_by: dict | None = None, order_by: str | list[str] | None = None):
        async with self.session_factory() as session:
            stmt = select(self.model)
            if filter_by:
                stmt = stmt.filter_by(**filter_by)
            if order_by:
                if isinstance(order_by, str):
                    order_by = [order_by]  # Преобразуем строку в список для единообразия
                order_clauses = []
                for field_spec in order_by:
                    if field_spec.startswith("-"):
                        field_name = field_spec[1:]
                        direction = "desc"
                    else:
                        field_name = field_spec
                        direction = "asc"

                    field = getattr(self.model, field_name, None)
                    if field is not None:
                        order_clauses.append(
                            field.desc() if direction == "desc" else field.asc()
                        )
                    else:
                        raise InvalidRequestError(f'Entity namespace for "{self.model.__tablename__}" has no property "{field_name}"')
                if order_clauses:
                    stmt = stmt.order_by(*order_clauses)
            res = await session.execute(stmt)
            return [row[0].to_read_model() for row in res.all()]

    async def get_first(self):
        raise NotImplementedError()

    async def get_info(self):
        raise NotImplementedError()

    async def get_one_by_username(self):
        raise NotImplementedError()