from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
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


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_one(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            if not res:
                return None
            return res.to_read_model()

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, id: int, data: dict) -> int | None:
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def delete_one(self, id: int) -> int | None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_all(self, filter_by: dict | None = None, order_by: str | list[str] | None = None): #  добавить filter_by
        async with async_session_maker() as session:
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
                if order_clauses:
                    stmt = stmt.order_by(*order_clauses)
            res = await session.execute(stmt)
            return [row[0].to_read_model() for row in res.all()]

    async def get_first(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars.first()