from pydantic import BaseModel

class SGetProduct(BaseModel):
    name: str
    description: str
    price: int
    first_image: str
    second_image: str
    third_image: str
