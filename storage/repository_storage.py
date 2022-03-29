import os
import csv
from collections import defaultdict

from typing import Dict, Set, List

from storage.singleton_metaclass import SingletonMeta


class RepositoryStorage(metaclass=SingletonMeta):
    filename = os.path.join("storage", "data", "repository.csv")
    headers = ["channel_id", "repository"]

    def __init__(self):
        self.__create_file()

        self.data = self.__read_file()

    def add_data(self, repositories: Dict[str, Set[str]]):
        self.data.update(repositories)
        self.__write_file(repositories)

    def  add_repository_to_channel(self, channel_id: str, repository: str):
        self.data[repository].add(channel_id)
        self.__write_file(self.data)

    def unsubscribe_channel_from_repository(self, channel_id: str, repository: str):
        self.data[repository].remove(channel_id)
        if not self.data[repository]:
            del self.data[repository]
        self.__write_file(self.data)

    def unsubscribe_channel_from_all_repository(self, channel_id: str):
        for repository in self.data.copy():
            if channel_id in self.data[repository].copy():
                self.data[repository].remove(channel_id)
                if not self.data[repository]:
                    del self.data[repository]
        self.__write_file(self.data)

    def get_repositories_by_channel_id(self, channel_id: str) -> Set[str]:
        repositories = {repository for repository in self.data if channel_id in self.data[repository]}
        return repositories

    def get_channels_by_repository_name(self, repo_name: str) -> Set[str]:
        return self.data[repo_name]

    def __create_file(self):
        if os.path.exists(self.filename):
            return

        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

    def __write_file(self, data: Dict[str, Set[str]]):
        with open(self.filename, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
            for repository in data:
                writer.writerows([[channel, repository] for channel in data[repository]])

    def __read_file(self) -> Dict[str, Set[str]]:
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            content = defaultdict(set)
            for row in reader:
                content[row["repository"]].add(row["channel_id"])
        return content
