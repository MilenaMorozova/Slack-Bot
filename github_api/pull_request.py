from typing import Optional, List
from datetime import datetime

from .user import User


class PullRequest:
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self):
        self.title: Optional[str] = None
        self.url: Optional[str] = None
        self.state: Optional[str] = None
        self.author: Optional[User] = None
        self.reviewers: List[User] = []
        self.created: Optional[datetime] = None
        self.updated: Optional[datetime] = None
        self.closed: Optional[datetime] = None
        self.merged: Optional[bool] = None
        self.mergeable: Optional[bool] = None
        self.repo_name: Optional[str] = None
        self.repo_full_name: Optional[str] = None

    @staticmethod
    def from_github_event(pull_request_data: dict) -> 'PullRequest':
        def parse_date(date: Optional[str]) -> Optional[datetime]:
            if date is None:
                return None
            return datetime.strptime(date, PullRequest.DATE_FORMAT)

        pull_request = PullRequest()
        pull_request.title = pull_request_data.get('title')
        pull_request.url = pull_request_data.get('url')
        pull_request.state = pull_request_data.get('state')
        pull_request.author = User.from_dict(pull_request_data.get('user'))
        pull_request.reviewers = list(map(User.from_dict, pull_request_data.get('requested_reviewers')))
        pull_request.created = parse_date(pull_request_data.get('created_at'))
        pull_request.updated = parse_date(pull_request_data.get('updated_at'))
        pull_request.closed = parse_date(pull_request_data.get('closed_at'))
        pull_request.merged = bool(pull_request_data['merged']) if 'merged' in pull_request_data else None
        pull_request.mergeable = bool(pull_request_data['mergeable']) if 'mergeable' in pull_request_data else None
        head = pull_request_data.get('head')
        if head:
            repo = head.get('repo')
            if repo:
                pull_request.repo_name = repo.get('name')
                pull_request.repo_full_name = repo.get('full_name')

        return pull_request
