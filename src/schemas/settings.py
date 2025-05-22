import datetime
from pydantic import BaseModel

class SDeskColorOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SFrameColorOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SLengthOut(BaseModel):
    id: int
    value: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SDepthOut(BaseModel):
    id: int
    value: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

