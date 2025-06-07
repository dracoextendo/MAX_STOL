import datetime
import re
from fastapi import HTTPException
from fastapi.params import Form
from pydantic import BaseModel, EmailStr, field_validator


class SOrderIn(BaseModel):
    username: str
    phone: str
    email: EmailStr | None
    telegram: str | None
    product_name: str
    desk_color: str
    frame_color: str
    depth: str
    length: str

    @field_validator('phone', mode='before')
    def validate_russian_phone(cls, v):
        cleaned_phone = re.sub(r'\D', '', v)

        if not re.fullmatch(r'^(\+?7|8)\d{10}$', cleaned_phone):
            raise HTTPException(status_code=422, detail="Invalid phone number")

        formatted_phone = f'+7{cleaned_phone[1:]}' if cleaned_phone.startswith(
            '8') else f'+{cleaned_phone}' if cleaned_phone.startswith('7') else cleaned_phone
        return formatted_phone

    @classmethod
    def as_form(cls,
                username: str = Form(min_length=2, max_length=255),
                phone: str = Form(examples=["+79999999999"]),
                email: EmailStr | None  = Form(default=None),
                telegram: str | None = Form(default=None, max_length=64),
                product_name: str = Form(),
                desk_color: str = Form(),
                frame_color: str = Form(),
                depth: str = Form(),
                length: str = Form()):
        return cls(
            username=username,
            phone=phone,
            email=email,
            telegram=telegram,
            product_name=product_name,
            desk_color=desk_color,
            frame_color=frame_color,
            depth=depth,
            length=length
        )

class SOrderOut(BaseModel):
    id: int
    username: str
    phone: str
    email: EmailStr | None
    telegram: str | None
    product_name: str
    desk_color: str
    frame_color: str
    depth: str
    length: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sort: int