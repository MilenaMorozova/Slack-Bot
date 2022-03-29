import os
import csv


class GithubToSlackUsersStorage:
    def __init__(self):
        self.filename = os.path.join("storage", "data", "github_to_slack_users.csv")
        self.headers = ["github_username", "slack_user_id"]
        self.__create_file()

        self.data = self.__read_file(self.filename)

    def add_data(self, usernames):
        self.data.update(usernames)
        self.__write_file(self.filename, usernames)

    def add_github_username(self, github_username, slack_user_id):
        self.data[github_username] = slack_user_id
        self.__write_file(self.filename, self.data)

    def replace_github_username(self, slack_user_id, github_username):
        for github_user in self.data:
            if self.data[github_user] == slack_user_id:
                del self.data[github_user]
                self.data[github_username] = slack_user_id
                break

        self.__write_file(self.filename, self.data)

    def delete_github_user(self, slack_user_id):
        for github_username in self.data:
            if self.data[github_username] == slack_user_id:
                del self.data[github_username]
                break

        self.__write_file(self.filename, self.data)

    def is_subscribed_github_user(self, github_username):
        return github_username in self.data

    def get_slack_user_id_by_github_username(self, github_username):
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

    def __write_file(self, filename, data):
        with open(filename, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

            for github_username in data:
                writer.writerow([github_username, data[github_username]])

    def __read_file(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            content = {row["github_username"]: row["slack_user_id"] for row in reader}
        return content
