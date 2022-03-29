from typing import List, Dict
from unittest import TestCase

from storage.users_storage import GithubToSlackUsersStorage
from storage.singleton_metaclass import SingletonMeta


class TestGithubToSlackUsersStorage(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        GithubToSlackUsersStorage()

    def tearDown(self) -> None:
        GithubToSlackUsersStorage().data = {}
        with open(GithubToSlackUsersStorage.filename, 'w') as file:
            file.write('')

    @classmethod
    def tearDownClass(cls) -> None:
        SingletonMeta._instances = {}

    def __read_lines(self) -> List[str]:
        with open(GithubToSlackUsersStorage.filename, 'r') as file:
            return list(map(str.strip, file.readlines()))

    def __check_state(self, data: Dict[str, str]):
        self.assertEqual(GithubToSlackUsersStorage().data, data)

        lines = self.__read_lines()
        self.assertEqual(len(lines), len(data) + 1)
        self.assertEqual(lines[0], ','.join(GithubToSlackUsersStorage.headers))

        for i, (key, value) in enumerate(data.items(), 1):
            self.assertEqual(lines[i], f'{key},{value}')

    def test_add_data(self):
        storage = GithubToSlackUsersStorage()
        storage.add_data({'git_name': 'slack_id'})
        self.__check_state({'git_name': 'slack_id'})

    def test_add_github_username(self):
        storage = GithubToSlackUsersStorage()
        storage.add_github_username('git_name', 'slack_id')
        self.__check_state({'git_name': 'slack_id'})

    def test_replace_github_username(self):
        storage = GithubToSlackUsersStorage()
        storage.add_github_username('git_name', 'slack_id')
        storage.replace_github_username('slack_id', 'git_name2')
        self.__check_state({'git_name2': 'slack_id'})

    def test_delete_github_user(self):
        storage = GithubToSlackUsersStorage()
        storage.add_github_username('git_name', 'slack_id')
        storage.delete_github_user('slack_id')
        self.__check_state({})

    def test_is_subscribed_github_user(self):
        storage = GithubToSlackUsersStorage()
        storage.add_github_username('git_name', 'slack_id')
        self.assertTrue(storage.is_subscribed_github_user('git_name'))
        self.assertFalse(storage.is_subscribed_github_user('git_name2'))
        self.__check_state({'git_name': 'slack_id'})

    def test_get_slack_user_id_by_github_username(self):
        storage = GithubToSlackUsersStorage()
        storage.add_github_username('git_name', 'slack_id')
        self.assertEqual(storage.get_slack_user_id_by_github_username('git_name'), 'slack_id')
        self.__check_state({'git_name': 'slack_id'})
