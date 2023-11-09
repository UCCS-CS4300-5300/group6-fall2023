from .extensions.error import RequestError
from .extensions.general.accounts import Accounts
from .extensions.general.media import Posts
from .extensions.general.me import Me
from .facebook import facebook_API
from .facebook_settings import facebook_Config
from django.test import TestCase


class facebook_APITest(TestCase):

    def setUp(self):
        self.facebook_api = facebook_API("123", facebook_Config())

    def test_set_token(self):
        token = "test"
        self.facebook_api.set_token(token)
        self.assertEqual(self.facebook_api.token, token)
        self.assertEqual(self.facebook_api.required_params, {'access_token': token})

    def test_get_posts(self):
        resp = self.facebook_api.general.get_accounts()
        self.assertIsInstance(resp, RequestError)

    def test_get_posts(self):
        resp = self.facebook_api.general.get_posts()
        self.assertIsInstance(resp, RequestError)

    def mock_get_me(self, endpoint, object_return_type):
        return Me.from_dict({
            "name": "test",
            "id": "test"
        })
    
    def mock_get_accounts(self, endpoint, object_return_type):
        return Accounts.from_dict({
            "data": [
                {
                "access_token": "1234",
                "category": "School",
                "category_list": [
                    {
                    "id": "2601",
                    "name": "School"
                    }
                ],
                "name": "Test page",
                "id": "130076146861171",
                "tasks": [
                    "ADVERTISE",
                    "ANALYZE",
                    "CREATE_CONTENT",
                    "MESSAGING",
                    "MODERATE",
                    "MANAGE"
                ]
                }
            ],
            "paging": {
                "cursors": {
                "before": "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxXUHpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3",
                "after": "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxXUHpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3"
                }
            }
        })
    
    def test_get_me(self):
        self.facebook_api.get = self.mock_get_me
        resp = self.facebook_api.general.get_me()
        self.assertIsInstance(resp, Me)

    def test_get_accounts(self):
        self.facebook_api.get = self.mock_get_accounts
        resp = self.facebook_api.general.get_accounts()
        self.assertIsInstance(resp, Accounts)
        self.assertEqual(resp.data[0].access_token, "1234")

    def test_fail_request_oauth(self):
        resp = self.facebook_api.get("test")
        self.assertIsInstance(resp, RequestError)
        self.assertEqual(resp.error.type, "OAuthException")







