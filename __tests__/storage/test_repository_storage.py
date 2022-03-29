from collections import defaultdict
from typing import List, Dict, Set
from unittest import TestCase

from storage.repository_storage import RepositoryStorage
from storage.singleton_metaclass import SingletonMeta


class TestRepositoryStorage(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        RepositoryStorage()

    def tearDown(self) -> None:
        RepositoryStorage().data = defaultdict(set)
        with open(RepositoryStorage.filename, 'w') as file:
            file.write('')

    @classmethod
    def tearDownClass(cls) -> None:
        SingletonMeta._instances = {}

    def __read_lines(self) -> List[str]:
        with open(RepositoryStorage.filename, 'r') as file:
            return list(map(str.strip, file.readlines()))

    def __check_state(self, data: Dict[str, Set[str]]):
        self.assertEqual(RepositoryStorage().data, data)

        lines = self.__read_lines()
        self.assertEqual(len(lines), len(data) + 1)
        self.assertEqual(lines[0], ','.join(RepositoryStorage.headers))

        i = 1
        for key, values in data.items():
            for value in values:
                self.assertEqual(lines[i], f'{value},{key}')
                i += 1

    def test_add_data(self):
        storage = RepositoryStorage()
        storage.add_data({'repo': {'chanel_id'}})
        self.__check_state({'repo': {'chanel_id'}})

    def test_add_repository_to_channel(self):
        storage = RepositoryStorage()
        storage.add_repository_to_channel('chanel_id', 'repo')
        self.__check_state({'repo': {'chanel_id'}})

    def test_unsubscribe_channel_from_repository(self):
        storage = RepositoryStorage()
        storage.add_repository_to_channel('chanel_id', 'repo')
        storage.add_repository_to_channel('chanel_id', 'repo2')
        self.__check_state({'repo': {'chanel_id'}, 'repo2': {'chanel_id'}})
        storage.unsubscribe_channel_from_repository('chanel_id', 'repo')
        self.__check_state({'repo2': {'chanel_id'}})

    def test_unsubscribe_channel_from_all_repository(self):
        storage = RepositoryStorage()
        storage.add_repository_to_channel('chanel_id', 'repo')
        storage.add_repository_to_channel('chanel_id', 'repo2')
        self.__check_state({'repo': {'chanel_id'}, 'repo2': {'chanel_id'}})
        storage.unsubscribe_channel_from_all_repository('chanel_id')
        self.__check_state({})

    def test_get_repositories_by_channel_id(self):
        storage = RepositoryStorage()
        storage.add_repository_to_channel('chanel_id', 'repo')
        self.assertEqual({'repo'}, storage.get_repositories_by_channel_id('chanel_id'))
        self.__check_state({'repo': {'chanel_id'}})

    def test_get_channels_by_repository_name(self):
        storage = RepositoryStorage()
        storage.add_repository_to_channel('chanel_id', 'repo')
        self.assertEqual({'chanel_id'}, storage.get_channels_by_repository_name('repo'))
        self.__check_state({'repo': {'chanel_id'}})
