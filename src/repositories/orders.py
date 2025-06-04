from src.models.orders import OrdersModel
from src.utils.repository import SQLAlchemyRepository


class OrdersRepository(SQLAlchemyRepository):
    model = OrdersModel