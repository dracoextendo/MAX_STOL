from src.schemas.orders import SOrderIn
from src.utils.repository import AbstractRepository


class OrdersService:
    def __init__(self, orders_repository: type[AbstractRepository]):
        self.orders_repository: AbstractRepository = orders_repository()

    async def get_order(self, id: int):
        order = await self.orders_repository.get_one(id)
        return order

    async def add_order(self, order: SOrderIn):
        orders_dict = order.model_dump()
        order_id = await self.orders_repository.add_one(orders_dict)
        return order_id

    async def update_order(self, id: int, order: SOrderIn) -> int:
        orders_dict = order.model_dump()
        order_id = await self.orders_repository.update_one(id, orders_dict)
        return order_id

    async def delete_order(self, id: int):
        order_id = await self.orders_repository.delete_one(id)
        return order_id

    async def get_all_orders(self):
        orders = await self.orders_repository.get_all(order_by = "-id")
        return orders