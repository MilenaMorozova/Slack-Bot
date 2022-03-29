import os
import csv

from typing import Dict

from storage.singleton_metaclass import SingletonMeta


class GithubToSlackUsersStorage(metaclass=SingletonMeta):
    filename = os.path.join("storage", "data", "github_to_slack_users.csv")
    headers = ["github_username", "slack_user_id"]

    def __init__(self):
        self.__create_file()
        self.data = self.__read_file()

    def add_data(self, usernames: Dict[str, str]):
        self.data.update(usernames)
        self.__write_file(usernames)

    def add_github_username(self, github_username: str, slack_user_id: str):
        self.data[github_username] = slack_user_id
        self.__write_file(self.data)

    def replace_github_username(self, slack_user_id: str, github_username: str):
        for github_user in self.data:
            if self.data[github_user] == slack_user_id:
                del self.data[github_user]
                self.data[github_username] = slack_user_id
                break

        self.__write_file(self.data)

    def delete_github_user(self, slack_user_id: str):
        for github_username in self.data:
            if self.data[github_username] == slack_user_id:
                del self.data[github_username]
                break

        self.__write_file(self.data)

    def is_subscribed_github_user(self, github_username: str) -> bool:
        return github_username in self.data

    def get_slack_user_id_by_github_username(self, github_username: str) -> str:
        return self.data[github_username]

    def __create_file(self):
        if os.path.exists(self.filename):
            return

        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

    def __write_file(self, data: Dict[str, str]):
        with open(self.filename, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

            for github_username in data:
                writer.writerow([github_username, data[github_username]])

    def __read_file(self) -> Dict[str, str]:
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            content = {row["github_username"]: row["slack_user_id"] for row in reader}
        return content
