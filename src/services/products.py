from src.schemas.products import SProductIn
from src.utils.repository import AbstractRepository


class ProductsService:
    def __init__(self, products_repository: type[AbstractRepository]):
        self.products_repository: AbstractRepository = products_repository()

    async def get_all_products(self, filter_by: dict | None = None, order_by: str | list[str] | None = None):
        products = await self.products_repository.get_all(filter_by, order_by)
        return products

    async def get_product(self, id: int):
        product = await self.products_repository.get_one(id)
        return product

    async def delete_product(self, id: int):
        files_to_delete = await self.products_repository.delete_one(id)
        return files_to_delete

    async def get_info(self, id: int):
        product = await self.products_repository.get_info(id)
        return product

    async def add_product(self, product: SProductIn, images_url: tuple[str, str, str]) -> int:
        product_dict = product.model_dump()
        product_dict['first_image'] = images_url[0]
        product_dict['second_image'] = images_url[1]
        product_dict['third_image'] = images_url[2]
        product_id = await self.products_repository.add_one(product_dict)
        return product_id

    async def update_product(self, id: int, product: SProductIn, images_url: tuple[str, str, str]):
        product_dict = product.model_dump()
        product_dict['first_image'] = images_url[0]
        product_dict['second_image'] = images_url[1]
        product_dict['third_image'] = images_url[2]
        product_id = await self.products_repository.update_one(id, product_dict)
        return product_id

