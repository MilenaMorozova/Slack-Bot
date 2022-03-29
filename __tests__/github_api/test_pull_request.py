from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch

from github_api import PullRequest


TEST_DATE = datetime.now()
TEST_DATE -= timedelta(microseconds=TEST_DATE.microsecond)

PULL_REQUEST_DATA = {
    "title": "title",
    "html_url": "url",
    "state": "state",
    "user": "author",
    "requested_reviewers": ["reviewers1", "reviewers2"],
    "created_at": TEST_DATE.strftime(PullRequest.DATE_FORMAT),
    "updated_at": TEST_DATE.strftime(PullRequest.DATE_FORMAT),
    "closed_at": TEST_DATE.strftime(PullRequest.DATE_FORMAT),
    "merged": False,
    "mergeable": False,
    "head": {
        "repo": {
            "name": "repo_name",
            "full_name": "repo_full_name"
        }
    }
}


class TestPullRequest(TestCase):
    @patch('github_api.pull_request.User.from_dict', lambda x: x)
    def test_from_github_event(self):
        request = PullRequest.from_github_event(PULL_REQUEST_DATA)
        self.assertEqual(request.title, "title")
        self.assertEqual(request.url, "url")
        self.assertEqual(request.state, "state")
        self.assertEqual(request.title, "title")
        self.assertEqual(request.author, "author")
        self.assertEqual(request.reviewers, ["reviewers1", "reviewers2"])
        self.assertEqual(request.created, TEST_DATE)
        self.assertEqual(request.updated, TEST_DATE)
        self.assertEqual(request.closed, TEST_DATE)
        self.assertEqual(request.merged, False)
        self.assertEqual(request.mergeable, False)
        self.assertEqual(request.repo_name, "repo_name")
        self.assertEqual(request.repo_full_name, "repo_full_name")

    @patch('github_api.pull_request.User.from_dict', lambda x: x)
    def test_from_github_event_without_fields(self):
        request = PullRequest.from_github_event({"requested_reviewers": []})
        self.assertIsNone(request.title)
        self.assertIsNone(request.url)
        self.assertIsNone(request.state)
        self.assertIsNone(request.title)
        self.assertIsNone(request.author)
        self.assertEqual(request.reviewers, [])
        self.assertIsNone(request.created)
        self.assertIsNone(request.updated)
        self.assertIsNone(request.closed)
        self.assertIsNone(request.merged)
        self.assertIsNone(request.mergeable)
        self.assertIsNone(request.repo_name)
        self.assertIsNone(request.repo_full_name)

