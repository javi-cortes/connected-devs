from typing import Optional

import aiohttp


class Github:
    GITHUB_USER_ORGS_URL = "https://api.github.com/users/{}/orgs"

    def __init__(self) -> None:
        super().__init__()

        self.organizations_in_common = []

    async def get_user_organizations(self, user: str) -> set:
        url = self.GITHUB_USER_ORGS_URL.format(user)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return self.parse_github_response(await response.json())

    @staticmethod
    def parse_github_response(response: dict) -> Optional[set]:
        if not isinstance(response, list):
            # not valid github member
            return None

        return {(org["id"], org["login"]) for org in response}
