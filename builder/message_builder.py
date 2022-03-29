from datetime import datetime
import json
import os

from typing import List, Tuple

from github_api import User
from storage.users_storage import GithubToSlackUsersStorage


class MessageBuilder:
    def __init__(self):
        self.users_storage = GithubToSlackUsersStorage()
        self.filename = os.path.join("builder", "message_template.json")
        self.content = self.__read_message_template()
        self.date_format = "%Y-%m-%d %H:%M UTC+0"

    def set_link_to_pull_request(self, link_to_pull_request: str) -> "MessageBuilder":
        self.content = self.content.replace("<link_to_pull_request>", link_to_pull_request)
        return self

    def set_pull_request_title(self, pull_request_title: str) -> "MessageBuilder":
        self.content = self.content.replace("<pull_request_title>", pull_request_title)
        return self

    def set_author(self, author: str) -> "MessageBuilder":
        self.content = self.content.replace("<author>", author)
        return self

    def set_repo_name(self, repo_name: str) -> "MessageBuilder":
        self.content = self.content.replace("<repo-name>", repo_name)
        return self

    def set_update_date(self, update_date: datetime) -> "MessageBuilder":
        self.content = self.content.replace("<update_date>", update_date.strftime(self.date_format))
        return self

    def set_create_date(self, create_date: datetime) -> "MessageBuilder":
        self.content = self.content.replace("<create_date>", create_date.strftime(self.date_format))
        return self

    def set_reviewers(self, *reviewers: Tuple[User, ...]) -> "MessageBuilder":
        if reviewers:
            result_reviewers = self.__convert_reviewers(*reviewers)
            self.content = self.content.replace("<reviewers>", ", ".join(result_reviewers))
        else:
            self.content = self.content.replace("<reviewers>", "No reviewers")
        return self

    def build(self) -> str:
        ready_message = json.loads(self.content)
        self.content = self.__read_message_template()
        return ready_message

    def __read_message_template(self) -> str:
        with open(self.filename, 'r') as file:
            content = file.read()
        return content

    def __convert_reviewers(self, reviewers: List[User]) -> List[str]:
        slack_reviewers = []
        for reviewer in reviewers:
            if self.users_storage.is_subscribed_github_user(reviewer.login):
                slack_user_id = self.users_storage.get_slack_user_id_by_github_username(reviewer.login)
                slack_reviewers.append(f"<@{slack_user_id}>")
            else:
                slack_reviewers.append(reviewer.login)

        return slack_reviewers
        