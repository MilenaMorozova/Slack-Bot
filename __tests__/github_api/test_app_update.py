from unittest import TestCase
from unittest.mock import patch, MagicMock

from github_api.app_update import create_jwt, set_app_url


class Test(TestCase):
    @patch('github_api.app_update.jwt.encode')
    def test_create_jwt(self, jwt_encode_mock: MagicMock):
        create_jwt('api_id', 'rsa_private_key')
        jwt_encode_mock.assert_called_once()
        self.assertEqual(jwt_encode_mock.call_args[0][1], 'rsa_private_key')

    @patch('github_api.app_update.create_jwt', lambda *a: 'jwt_key')
    @patch('github_api.app_update.requests.patch')
    def test_set_app_url(self, patch_mock: MagicMock):
        set_app_url('url', 'api_id', 'rsa_private_key')
        patch_mock.assert_called_once()
