from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class RequestRegisterResponse(BaseModel):
    registered_at: Optional[datetime]
    connected: Optional[bool]
    organizations: Optional[List[str]] = []

    class Config:
        orm_mode = True


class RequestRegisterStorePayload(BaseModel):
    dev1: str
    dev2: str
    connected: Optional[bool]
    organizations: Optional[List[str]]
