from src.dao.base import BaseDAO
from src.models.products import ProductsModel


class ProductsDAO(BaseDAO):
    model = ProductsModel