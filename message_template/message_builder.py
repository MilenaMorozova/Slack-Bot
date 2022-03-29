import json
import os


class MessageBuilder:
    def __init__(self):
        self.filename = os.path.join("message_template", "message_template.json")
        self.content = self.__read_message_template()

    def __read_message_template(self):
        with open(self.filename, 'r') as file:
            content = file.read()
        return content

    def set_link_to_pull_request(self, link_to_pull_request):
        self.content = self.content.replace("<link_to_pull_request>", link_to_pull_request)
        return self

    def set_pull_request_title(self, pull_request_title):
        self.content = self.content.replace("<pull_request_title>", pull_request_title)
        return self

    def set_author(self, author):
        self.content = self.content.replace("<author>", author)
        return self

    def set_repo_name(self, repo_name):
        self.content = self.content.replace("<repo-name>", repo_name)
        return self

    def set_update_date(self, update_date):
        self.content = self.content.replace("<update_date>", update_date)
        return self

    def set_create_date(self, create_date):
        self.content = self.content.replace("<create_date>", create_date)
        return self

    def set_reviewers(self, *reviewers):
        if reviewers:
            self.content = self.content.replace("<reviewers>", ", ".join(*reviewers))
        else:
            self.content = self.content.replace("<reviewers>", "No reviewers")
        return self

    def build(self):
        ready_message = json.loads(self.content)
        self.content = self.__read_message_template()
        return ready_message
        