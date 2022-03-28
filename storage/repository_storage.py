import os
import csv
from collections import defaultdict


class RepositoryStorage:
    def __init__(self):
        self.filename = os.path.join("storage", "data", "repository.csv")
        self.headers = ["channel_id", "repository"]
        self.__create_file()

        self.data = self.__read_file(self.filename)

    def add_data(self, repositories):
        self.data.update(repositories)
        self.__write_file(self.filename, repositories)

    def add_repository_to_channel(self, channel_id, repository):
        self.data[repository].add(channel_id)
        self.__write_file(self.filename, self.data)

    def unsubscribe_channel_from_repository(self, channel_id, repository):
        self.data[repository].remove(channel_id)
        self.__write_file(self.filename, self.data)

    def unsubscribe_channel_from_all_repository(self, channel_id):
        for repository in self.data:
            if channel_id in self.data[repository]:
                self.data[repository].remove(channel_id)

    def get_repositories_by_channel_id(self, channel_id):
        repositories = [repository for repository in self.data if channel_id in self.data[repository]]
        return repositories

    def get_user_id_by_email(self, email):
        return self.data[email]

    def get_user_ids_by_emails(self, emails):
        return [self.data[email] for email in emails]

    def __create_file(self):
        if os.path.exists(self.filename):
            return

        with open(self.filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

    def __write_file(self, filename, data):
        with open(filename, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
            for repository in data:
                writer.writerows([[channel, repository] for channel in data[repository]])

    def __read_file(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            content = defaultdict(set)
            for row in reader:
                content[row["repository"]].add(row["channel_id"])
        return content
