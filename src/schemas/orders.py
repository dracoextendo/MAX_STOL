import datetime

from pydantic import BaseModel, Field, ConfigDict


class SCreateOrder(BaseModel):
    username: str
    phone: str
    email: str | None
    telegram: str | None
    product_name: str
    desk_color: str
    frame_color: str
    depth: str
    width: str

class SGetOrder(SCreateOrder):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)