from unittest.mock import AsyncMock, patch, MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.twitter import TwitterUser


def test_connected_without_user(client: TestClient, db: Session):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/",
    )
    assert response.status_code == 404


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=False,
)
@patch(
    "app.services.connected.ConnectedService.handle_connection_on_twitter",
    return_value=True,
)
def test_devs_connected_only_twitter(
    twitter: AsyncMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected") is False


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.handle_connection_on_twitter",
    return_value=False,
)
def test_devs_connected_only_github(
    twitter: AsyncMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected") is False


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=False,
)
@patch(
    "app.services.connected.ConnectedService.handle_connection_on_twitter",
    return_value=False,
)
def test_devs_not_connected(
    twitter: AsyncMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected") is False


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.handle_connection_on_twitter",
    return_value=True,
)
def test_devs_connected(
    twitter: AsyncMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected")


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.get_twitter_info_from",
    side_effect=[
        TwitterUser(user_id=1, username="pepe", valid_user=True, followers=[1, 2, 3]),
        TwitterUser(user_id=2, username="pepa", valid_user=True, followers=[1, 2, 3]),
    ],
)
def test_devs_connected_that_they_follow_on_twitter(
    get_twitter_info_from: MagicMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected")


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.get_twitter_info_from",
    side_effect=[
        TwitterUser(user_id=1, username="pepe", valid_user=True, followers=[]),
        TwitterUser(user_id=2, username="pepa", valid_user=True, followers=[]),
    ],
)
def test_devs_connected_that_they_dont_follow_on_twitter(
    get_twitter_info_from: MagicMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected") is False


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.get_twitter_info_from",
    side_effect=[
        TwitterUser(user_id=1, username="pepe", valid_user=True, followers=[2]),
        TwitterUser(user_id=2, username="pepa", valid_user=True, followers=[]),
    ],
)
def test_devs_connected_that_they_only_one_follows_the_other(
    get_twitter_info_from: MagicMock, github: AsyncMock, client: TestClient, db: Session
):
    response = client.post(
        f"{settings.API_V1_STR}/connected/a/b",
    )

    assert response.status_code == 200
    response = response.json()
    assert response.get("connected") is False


@patch(
    "app.services.connected.ConnectedService.handle_connection_on_github",
    return_value=True,
)
@patch(
    "app.services.connected.ConnectedService.get_twitter_info_from",
    side_effect=[
        TwitterUser(user_id=1, username="pepe", valid_user=False, followers=[2]),
        TwitterUser(user_id=2, username="pepa", valid_user=True, followers=[]),
    ],
)
def test_devs_connected_twitter_user_not_valid(
    get_twitter_info_from: MagicMock, github: AsyncMock, client: TestClient, db: Session
):
    dev1 = "a"
    dev2 = "b"
    response = client.post(
        f"{settings.API_V1_STR}/connected/{dev1}/{dev2}",
    )

    assert response.status_code == 200
    response = response.json()
    print(response)
    assert response.get("connected") is False
    errors = response.get("errors")[0]
    assert dev1 in errors
    assert "twitter" in errors
