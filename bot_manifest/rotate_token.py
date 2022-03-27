import requests
import json

from constants import REFRESH_TOKEN


def update_token_constant(constant_name, new_value):
    with open("constants.py", 'r') as file:
        content = file.readlines()

    with open("constants.py", 'w') as file:
        for i, value in enumerate(content):
            if value.startswith(constant_name):
                split_string = value.split()
                split_string[-1] = f'"{new_value}"\n'
                content[i] = " ".join(split_string)
                break

        file.write("".join(content))


def rotate_token():
    response = requests.get("https://slack.com/api/tooling.tokens.rotate",
                            params={"refresh_token": REFRESH_TOKEN},
                            headers={"Content-Type": "application/x-www-form-urlencoded"})

    response_data = json.loads(response.content)
    if response_data["ok"]:
        access_token = response_data["token"]
        refresh_token = response_data["refresh_token"]

        update_token_constant("ACCESS_TOKEN", access_token)
        update_token_constant("REFRESH_TOKEN", refresh_token)
