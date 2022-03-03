from pydantic import BaseModel
from typing import Optional, List


class ConnectedQuery(BaseModel):
    dev1: str
    dev2: str


class ConnectedResult(BaseModel):
    connected: bool
    organizations: Optional[List[str]] = []
    errors: Optional[List[str]] = []
