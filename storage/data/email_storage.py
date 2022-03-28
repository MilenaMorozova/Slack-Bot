import os
import csv


class EmailStorage:
    def __init__(self):
        self.filename = os.path.join("storage", "data", "email.csv")
        self.headers = ["user_id", "email"]
        self.__create_file()

        self.data = self.__read_file(self.filename)

    def add_data(self, emails):
        self.data.update(emails)
        self.__write_file(self.filename, emails)

    def add_email(self, user_id, email):
        self.data[email] = user_id
        self.__write_file(self.filename, self.data)

    def replace_email(self, user_id, email):
        for user_email in self.data:
            if self.data[user_email] == user_id:
                del self.data[user_email]
                self.data[email] = user_id
                break

        self.__write_file(self.filename, self.data)

    def delete_email(self, email):
        del self.data[email]
        self.__write_file(self.filename, self.data)

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
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
            for email in data:
                writer.writerow([data[email], email])

    def __read_file(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            content = {row["email"]: row["user_id"] for row in reader}
        return content
