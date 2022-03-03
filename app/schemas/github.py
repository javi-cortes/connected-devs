from typing import List

from app.schemas.base_user import BaseUser


class GithubUser(BaseUser):
    organizations: List[str] = []
