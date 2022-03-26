from typing import Callable, List
from datetime import datetime
from time import sleep

from github import Github, PullRequest
from github.Repository import Repository
from github.PullRequest import PullRequest


class Api:
    def __init__(self, personal_access_token: str, repo_name: str, after_date: datetime = None):
        if after_date is None:
            after_date = datetime.now()
        self._after_date = after_date
        self._repo_name = repo_name
        self._github: Github = Github(personal_access_token)
        self._is_started = False
        self.on_merge_request: List[Callable[[PullRequest], None]] = []

    def start(self):
        self._is_started = True
        while self._is_started:
            if self.on_merge_request:
                self._check_merge_requests()

            self._after_date = datetime.now()
            sleep(30)

    def _check_merge_requests(self):
        for request in self._get_open_merge_requests():
            if request.created_at <= self._after_date:
                break

            for observer in self.on_merge_request:
                observer(request)

    def _get_repository(self) -> Repository:
        return self._github.get_repo(self._repo_name, True)

    def _get_open_merge_requests(self) -> List[PullRequest]:
        return list(self._get_repository().get_pulls(state='open', sort='updated', direction='desc'))
