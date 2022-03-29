from unittest import TestCase

from github_api import User


class TestUser(TestCase):
    def test_from_dict_with_email(self):
        user = User.from_dict({"login": "login", "id": "id", "mail": "mail"})
        self.assertEqual(user.login, "login")
        self.assertEqual(user.id, "id")
        self.assertEqual(user.mail, "mail")

    def test_from_dict_without_email(self):
        user = User.from_dict({"login": "login", "id": "id"})
        self.assertEqual(user.login, "login")
        self.assertEqual(user.id, "id")
        self.assertIsNone(user.mail)

    def test_from_dict_without_id(self):
        user = User.from_dict({"login": "login"})
        self.assertIsNone(user)

    def test_from_dict_without_login(self):
        user = User.from_dict({"id": "id"})
        self.assertIsNone(user)
