from typing import List, Callable

from flask import Flask, request
from typer.models import AnyType

from .pull_request import PullRequest


class _GithubEventController:
    def __init__(self):
        self.on_open_pull_request: List[Callable[[PullRequest], AnyType]] = []
        self.on_edit_pull_request: List[Callable[[PullRequest], AnyType]] = []

    def invoke_open_pull_request(self, req: PullRequest):
        for listener in self.on_open_pull_request:
            listener(req)

    def invoke_edit_pull_request(self, req: PullRequest):
        for listener in self.on_open_pull_request:
            listener(req)


_githubEventController = _GithubEventController()


def get_event_controller() -> _GithubEventController:
    return _githubEventController


def add_routs(app: Flask):
    @app.route("/github/events", methods=["POST"])
    def events():
        global _githubEventController
        pull_request = PullRequest.from_github_event(request.json['pull_request'])

        if request.json['action'] == 'opened':
            _githubEventController.invoke_open_pull_request(pull_request)

        if request.json['action'] == 'edited':
            _githubEventController.invoke_edit_pull_request(pull_request)

        return 'Response'
