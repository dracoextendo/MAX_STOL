from fastapi.params import Form
from pydantic import BaseModel


class SUserIn(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls,
                username: str = Form(min_length=2, max_length=255),
                password: str = Form(),
                ):
        return cls(
            username=username,
            password=password,
        )
