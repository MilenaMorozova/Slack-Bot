import requests
from datetime import timedelta, datetime
import jwt


def create_jwt(app_id: str, rsa_private_key: str) -> str:
    payload = {
        # issued at time, 60 seconds in the past to allow for clock drift
        "iat": int((datetime.now() - timedelta(seconds=60)).timestamp()),
        # JWT expiration time (10 minute maximum)
        "exp": int((datetime.now() + timedelta(minutes=3)).timestamp()),
        # GitHub App's identifier
        "iss": app_id
    }

    return jwt.encode(payload, rsa_private_key, algorithm="RS256")


def set_app_url(url: str, app_id: str, rsa_private_key: str):
    jwt_key = create_jwt(app_id, rsa_private_key)
    requests.patch(
        "https://api.github.com/app/hook/config",
        json={"url": f"{url}/github/events"},
        headers={"Authorization": f"Bearer {jwt_key}"}
    )
