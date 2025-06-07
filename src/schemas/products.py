import datetime
from fastapi import UploadFile
from fastapi.params import Form, File
from pydantic import BaseModel
from src.schemas.settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut


class SProductIn(BaseModel):
    name: str
    description: str
    price: int
    first_image: UploadFile
    second_image: UploadFile
    third_image: UploadFile
    desk_colors: list[int]
    frame_colors: list[int]
    lengths: list[int]
    depths: list[int]
    sort: int | None
    is_active: bool | None

    @classmethod
    def as_form(cls,
                name: str = Form(min_length=2, max_length=255),
                description: str = Form(min_length=2, max_length=1000),
                price: int = Form(),
                first_image: UploadFile = File(),
                second_image: UploadFile = File(),
                third_image: UploadFile = File(),
                desk_colors: list[int] = Form(),
                frame_colors: list[int] = Form(),
                lengths: list[int] = Form(),
                depths: list[int] = Form(),
                sort: int | None = Form(default=500),
                is_active: bool | None = Form(default=True),):
        return cls(
            name=name,
            description=description,
            price=price,
            first_image=first_image,
            second_image=second_image,
            third_image=third_image,
            desk_colors=desk_colors,
            frame_colors=frame_colors,
            lengths=lengths,
            depths=depths,
            sort=sort,
            is_active=is_active
        )

class SProductOut(BaseModel):
    id: int
    sort: int
    is_active: bool
    name: str
    description: str
    price: int
    first_image: str
    second_image: str
    third_image: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SProductInfoOut(BaseModel):
    product: SProductOut
    desk_colors: list[SDeskColorOut]
    frame_colors: list[SFrameColorOut]
    length: list[SLengthOut]
    depth: list[SDepthOut]
