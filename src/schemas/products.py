from pydantic import BaseModel, ConfigDict


class SGetDeskColors(BaseModel):
    id: int
    color: str

class SGetFrameColors(BaseModel):
    id: int
    color: str

class SGetDepth(BaseModel):
    id: int
    value: int

class SGetLength(BaseModel):
    id: int
    value: int

class SGetProduct(BaseModel):
    id: int
    name: str
    description: str
    price: int
    first_image: str
    second_image: str
    third_image: str

class SGetProductInfo(BaseModel):
    product: SGetProduct
    desk_colors: list[SGetDeskColors]
    frame_colors: list[SGetFrameColors]
    depth: list[SGetDepth]
    length: list[SGetLength]
