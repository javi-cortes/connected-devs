import os
from typing import Optional, List

import tweepy


class Twitter:
    def __init__(self) -> None:
        super().__init__()

        bearer_token = os.environ.get("TWITTER_API_BEARER_TOKEN")
        self.twitter = tweepy.Client(bearer_token)

    def get_user_id(self, dev) -> Optional[int]:
        try:
            response = self.twitter.get_user(username=dev)
        except tweepy.errors.HTTPException:
            response = None

        if not response or not response.data:
            return None

        return response.data.id

    def get_followers(self, dev: str) -> Optional[List[int]]:
        try:
            user_id = self.get_user_id(dev)
        except tweepy.errors.HTTPException:
            return None

        response = self.twitter.get_users_followers(user_id)
        if not response.data:
            return []

        return [user.id for user in response.data]
