from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    valid_user: bool = True
