from sqlalchemy.orm import Session

from app.integrations.github import Github
from app.integrations.twitter import Twitter
from app.schemas import ConnectedResult
from app.schemas.github import GithubUser
from app.schemas.twitter import TwitterUser
from app.services.main import AppService
from app.utils.service_result import ServiceResult


class ConnectedService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.github = Github()
        self.twitter = Twitter()
        self.connected_result = ConnectedResult(connected=True)

    async def check_connection_between(self, dev1, dev2) -> ServiceResult:
        if dev1 == dev2:
            return ServiceResult(ConnectedResult(connected=True))

        connected_on_twitter = await self.handle_connection_on_twitter(dev1, dev2)
        connected_on_github = await self.handle_connection_on_github(dev1, dev2)

        self.connected_result.connected = connected_on_github and connected_on_twitter

        return ServiceResult(self.connected_result)

    async def handle_connection_on_twitter(self, dev1, dev2) -> bool:
        """
        Handles connection on twitter, fills up connected_result info
        and returns whethere they're connected or not
        """
        twitter_dev1 = self.get_twitter_info_from(dev1)
        if not twitter_dev1.valid_user:
            self.connected_result.errors.append(
                f"{dev1} is not a valid user on twitter"
            )

        twitter_dev2 = self.get_twitter_info_from(dev2)
        if not twitter_dev2.valid_user:
            self.connected_result.errors.append(
                f"{dev2} is not a valid user on twitter"
            )

        dev1_follows_dev2 = twitter_dev1.user_id in twitter_dev2.followers
        dev2_follows_dev1 = twitter_dev2.user_id in twitter_dev1.followers

        return dev1_follows_dev2 and dev2_follows_dev1

    async def handle_connection_on_github(self, dev1, dev2) -> bool:
        """
        Handles connection on github, fills up connected_result info
        and returns whethere they're connected or not
        """
        github_dev1 = await self.get_github_info_from(dev1)
        if not github_dev1.valid_user:
            self.connected_result.errors.append(f"{dev1} is not a valid user on github")

        github_dev2 = await self.get_github_info_from(dev2)
        if not github_dev2.valid_user:
            self.connected_result.errors.append(f"{dev2} is not a valid user on github")

        if github_dev1.valid_user and github_dev2.valid_user:
            self.connected_result.organizations = set(github_dev1.organizations) & set(
                github_dev2.organizations
            )

        return bool(self.connected_result.organizations)

    async def get_github_info_from(self, dev: str) -> GithubUser:
        github_user = GithubUser(username=dev)

        github_user.organizations = await self.github.get_user_organizations(dev)
        if github_user.organizations is None:
            github_user.valid_user = False

        return github_user

    def get_twitter_info_from(self, dev: str) -> TwitterUser:
        twitter_user = TwitterUser(username=dev)

        twitter_user.user_id = self.twitter.get_user_id(dev)
        if twitter_user.user_id is None:
            twitter_user.valid_user = False
            return twitter_user

        twitter_user.followers = self.twitter.get_followers(dev)

        return twitter_user
