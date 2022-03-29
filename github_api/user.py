from typing import Optional


class User:
    def __init__(self, login: str, user_id: str, mail: Optional[str] = None):
        self.login = login
        self.id = user_id
        self.mail = mail

    @staticmethod
    def from_dict(data: Optional[dict]) -> Optional['User']:
        try:
            return User(data['login'], data['id'], data.get('mail'))
        except KeyError:
            return None
