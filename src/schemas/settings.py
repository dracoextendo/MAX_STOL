import datetime

from fastapi.params import Form
from pydantic import BaseModel

class SDeskColorIn(BaseModel):
    name: str
    sort: int | None

    @classmethod
    def as_form(cls,
                name: str = Form(min_length=2, max_length=255),
                sort: int | None = Form(default=500),
                ):
        return cls(
            name=name,
            sort=sort,
        )

class SFrameColorIn(BaseModel):
    name: str
    sort: int | None

    @classmethod
    def as_form(cls,
                name: str = Form(min_length=2, max_length=255),
                sort: int | None = Form(default=500),
                ):
        return cls(
            name=name,
            sort=sort,
        )

class SLengthIn(BaseModel):
    value: int
    sort: int | None

    @classmethod
    def as_form(cls,
                value: int = Form(),
                sort: int | None = Form(default=500),
                ):
        return cls(
            value=value,
            sort=sort,
        )

class SDepthIn(BaseModel):
    value: int
    sort: int | None

    @classmethod
    def as_form(cls,
                value: int = Form(),
                sort: int | None = Form(default=500),
                ):
        return cls(
            value=value,
            sort=sort,
        )

class SDeskColorOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sort: int

class SFrameColorOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sort: int

class SLengthOut(BaseModel):
    id: int
    value: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sort: int

class SDepthOut(BaseModel):
    id: int
    value: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sort: int

