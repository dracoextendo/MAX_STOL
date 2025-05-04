from pydantic import BaseModel, Field

class SCreateOrder(BaseModel):
    name: str
    phone: str
    product_id: int