import json

import requests

from constants import (
    HOST, ACCESS_TOKEN, SLACK_APP_ID, GITHUB_APP_ID, RSA_KEY
)
from github_api import set_app_url


def replace_host_in_manifest() -> str:
    with open("manifest.json", 'r') as file:
        content = file.read()
        content = content.replace("<host>", HOST)

    return content


def validate_bot_manifest(manifest_content: str) -> bool:
    response = requests.post("https://slack.com/api/apps.manifest.validate",
                             data={"token": ACCESS_TOKEN,
                                   "app_id": SLACK_APP_ID,
                                   "manifest": manifest_content})

    response_data = json.loads(response.content)
    if not response_data["ok"]:
        return False

    return True


def update_bot_manifest() -> bool:
    manifest_content = replace_host_in_manifest()

    if not validate_bot_manifest(manifest_content):
        return False

    response = requests.post("https://slack.com/api/apps.manifest.update",
                             data={"token": ACCESS_TOKEN,
                                   "app_id": SLACK_APP_ID,
                                   "manifest": manifest_content})

    response_data = json.loads(response.content)
    return response_data["ok"]


# print(update_bot_manifest())
# set_app_url(HOST, GITHUB_APP_ID, RSA_KEY)
