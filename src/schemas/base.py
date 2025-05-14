from pydantic import BaseModel

class SBaseStatus(BaseModel):
    status: str

class SLoginForm(BaseModel):
    username: str
    password: str