from src.schemas.individual_orders import SIndividualOrderIn
from src.utils.repository import AbstractRepository


class IndividualOrdersService:
    def __init__(self, individual_orders_repository: type[AbstractRepository]):
        self.individual_orders_repository: AbstractRepository = individual_orders_repository()

    async def get_order(self, id: int):
        order = await self.individual_orders_repository.get_one(id)
        return order

    async def add_order(self, order: SIndividualOrderIn):
        orders_dict = order.model_dump()
        order_id = await self.individual_orders_repository.add_one(orders_dict)
        return order_id

    async def update_order(self, id: int, order: SIndividualOrderIn) -> int:
        orders_dict = order.model_dump()
        order_id = await self.individual_orders_repository.update_one(id, orders_dict)
        return order_id

    async def delete_order(self, id: int):
        order_id = await self.individual_orders_repository.delete_one(id)
        return order_id

    async def get_all_orders(self, filter_by: dict | None = None, order_by: str | list[str] | None = None):
        orders = await self.individual_orders_repository.get_all(filter_by, order_by)
        return orders