from typing import List, Optional

from app.schemas.base_user import BaseUser


class TwitterUser(BaseUser):
    user_id: Optional[int]
    followers: List[int] = []
