from unittest.mock import patch
from facebook_api.extensions.error import RequestError
from facebook_api.extensions.general.accounts import Accounts
from facebook_api.extensions.general.me import Me
from facebook_api.extensions.general.businessAccounts import BusinessAccounts, InstagramBusinessAccount
from facebook_api.extensions.general.accounts import Accounts, CategoryList, Datum as DatumAccount, Paging
from facebook_api.extensions.general.media import Posts, Datum, Paging, Cursors
from facebook_api.extensions.authentication.extendToken import ExtendToken
from facebook_api.extensions.authentication.userAuth import UserAuth
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics
from facebook_api.extensions.general.postInfo import PostInfo

# TODO add barrel export to make this easier and cleaner

from facebook_api.facebook_settings import facebook_Config
from django.test import TestCase
from facebook_api.facebook import facebook_API


class facebook_APITest(TestCase):
    def setUp(self):
        self.facebook_api = facebook_API("123", facebook_Config())

    def test_set_token(self):
        token = "test"
        self.facebook_api.set_token(token)
        self.assertEqual(self.facebook_api.token, token)
        self.assertEqual(self.facebook_api.required_params,
                         {'access_token': token})

    def mock_get_me(self, endpoint, object_return_type):
        return Me.from_dict({"name": "test", "id": "test"})

    def mock_get_accounts(self, endpoint, object_return_type):
        return Accounts.from_dict({
            "data": [{
                "access_token":
                "1234",
                "category":
                "School",
                "category_list": [{
                    "id": "2601",
                    "name": "School"
                }],
                "name":
                "Test page",
                "id":
                "130076146861171",
                "tasks": [
                    "ADVERTISE", "ANALYZE", "CREATE_CONTENT", "MESSAGING",
                    "MODERATE", "MANAGE"
                ]
            }],
            "paging": {
                "cursors": {
                    "before":
                    "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxXUHpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3",
                    "after":
                    "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxXUHpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3"
                }
            }
        })
    
    def mock_get_posts(self):
        return Posts.from_dict({
            "data": [{
                "id": "123",
                "caption": "test",
                "media_type": "image",
                "media_url": "https://example.com",
                "permalink": "https://example.com",
                "timestamp": "2023-01-01T12:00:00",
                "like_count": 10,
                "comments_count": 5
            }],
            "paging": {
                "cursors": {
                    "before": "123",
                    "after": "456"
                }
            }
        })
    
    def test_get_posts(self):
        self.facebook_api.general.get_posts = self.mock_get_posts
        resp = self.facebook_api.general.get_posts()
        self.assertIsInstance(resp, Posts)
        self.assertEqual(resp.data[0].id, "123")

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
        resp = self.facebook_api.get("test", object_return_type=RequestError)
        self.assertIsInstance(resp, RequestError)
        self.assertEqual(resp.error.type, "OAuthException")

class facebook_me_tests(TestCase):
    def test_create_instance_with_valid_name_and_id(self):
        name = 'John'
        id = '123'
        me = Me(name, id)
        self.assertEqual(me.name, name)
        self.assertEqual(me.id, id) 


    def test_from_dict(self):
        obj = {
            'name': 'John',
            'id': '123'
        }
        self.assertEqual(me.name, 'John')
        self.assertEqual(me.id, '123') 


    def test_from_dict(self):
        # Arrange
        data = {
            'name': 'John',
            'id': '123'
        }
        expected_name = 'John'
        expected_id = '123'

        # Act
        result = Me.from_dict(data)

        # Assert
        self.assertIsInstance(result, Me)
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.id, expected_id)
    


    def test_from_dict(self):
        obj = {
            'name': 'John',
            'id': '123'
        }
        expected_name = 'John'
        expected_id = '123'

        me_instance = Me.from_dict(obj)

        self.assertEqual(me_instance.name, expected_name)
        self.assertEqual(me_instance.id, expected_id) 


    class Me:
        name: str
        id: str

        @staticmethod
        def from_dict(obj) -> 'Me':
            _name = str(obj.get("name"))
            _id = str(obj.get("id"))
            return Me(_name, _id)


        def test_to_dict(self):
            me = Me("John", "123")
            expected_dict = {"name": "John", "id": "123"}
            self.assertEqual(me.__dict__, expected_dict)
    


    def test_from_dict(self):
            obj = {
                'name': 'John',
                'id': '123'
            }
            expected_name = 'John'
            expected_id = '123'

            me_instance = Me.from_dict(obj)

            self.assertEqual(me_instance.name, expected_name)
            self.assertEqual(me_instance.id, expected_id) 


class Post_CursorsTestCase(TestCase):
    def test_from_dict(self):
        cursors_dict = {"before": "123", "after": "456"}
        cursors = Cursors.from_dict(cursors_dict)
        self.assertEqual(cursors.before, "123")
        self.assertEqual(cursors.after, "456")

class Post_DatumTestCase(TestCase):
    def test_from_dict(self):
        datum_dict = {"id": "789"}
        datum = Datum.from_dict(datum_dict)
        self.assertEqual(datum.id, "789")

class Post_PagingTestCase(TestCase):
    def test_from_dict(self):
        paging_dict = {"cursors": {"before": "123", "after": "456"}}
        paging = Paging.from_dict(paging_dict)
        self.assertEqual(paging.cursors.before, "123")
        self.assertEqual(paging.cursors.after, "456")

class Post_PostsTestCase(TestCase):
    def test_from_dict(self):
        posts_dict = {
            "data": [{"id": "789"}, {"id": "012"}],
            "paging": {"cursors": {"before": "123", "after": "456"}}
        }
        posts = Posts.from_dict(posts_dict)
        self.assertEqual(len(posts.data), 2)
        self.assertEqual(posts.data[0].id, "789")
        self.assertEqual(posts.data[1].id, "012")
        self.assertEqual(posts.paging.cursors.before, "123")
        self.assertEqual(posts.paging.cursors.after, "456")


class InstaAccounts_InstagramBusinessAccountTestCase(TestCase):
    def test_from_dict(self):
        data = {"id": "123"}
        instagram_business_account = InstagramBusinessAccount.from_dict(data)
        self.assertEqual(instagram_business_account.id, "123")

class InstaAccounts_BusinessAccountsTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "instagram_business_account": {"id": "456"},
            "id": "789"
        }
        business_accounts = BusinessAccounts.from_dict(data)
        self.assertEqual(business_accounts.id, "789")
        self.assertEqual(business_accounts.instagram_business_account.id, "456")



class Account_CategoryListTestCase(TestCase):
    def test_from_dict(self):
        data = {"id": "1", "name": "Category1"}
        category_list = CategoryList.from_dict(data)
        self.assertEqual(category_list.id, "1")
        self.assertEqual(category_list.name, "Category1")

class Account_CursorsTestCase(TestCase):
    def test_from_dict(self):
        data = {"before": "123", "after": "456"}
        cursors = Cursors.from_dict(data)
        self.assertEqual(cursors.before, "123")
        self.assertEqual(cursors.after, "456")

class Account_DatumTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "access_token": "abc123",
            "category": "Category",
            "category_list": [{"id": "1", "name": "Category1"}],
            "name": "John Doe",
            "id": "123",
            "tasks": ["task1", "task2"]
        }
        datum = DatumAccount.from_dict(data)
        self.assertEqual(datum.access_token, "abc123")
        self.assertEqual(datum.category, "Category")
        self.assertEqual(len(datum.category_list), 1)
        self.assertEqual(datum.category_list[0].id, "1")
        self.assertEqual(datum.category_list[0].name, "Category1")
        self.assertEqual(datum.name, "John Doe")
        self.assertEqual(datum.id, "123")
        self.assertEqual(len(datum.tasks), 2)
        self.assertEqual(datum.tasks[0], "task1")
        self.assertEqual(datum.tasks[1], "task2")

class Account_PagingTestCase(TestCase):
    def test_from_dict(self):
        data = {"cursors": {"before": "123", "after": "456"}}
        paging = Paging.from_dict(data)
        self.assertEqual(paging.cursors.before, "123")
        self.assertEqual(paging.cursors.after, "456")

class Account_AccountsTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "data": [
                {
                    "access_token": "abc123",
                    "category": "Category",
                    "category_list": [{"id": "1", "name": "Category1"}],
                    "name": "John Doe",
                    "id": "123",
                    "tasks": ["task1", "task2"]
                }
            ],
            "paging": {"cursors": {"before": "123", "after": "456"}}
        }
        accounts = Accounts.from_dict(data)
        self.assertEqual(len(accounts.data), 1)
        self.assertEqual(accounts.data[0].access_token, "abc123")
        self.assertEqual(accounts.data[0].category, "Category")
        self.assertEqual(len(accounts.data[0].category_list), 1)
        self.assertEqual(accounts.data[0].category_list[0].id, "1")
        self.assertEqual(accounts.data[0].category_list[0].name, "Category1")
        self.assertEqual(accounts.data[0].name, "John Doe")
        self.assertEqual(accounts.data[0].id, "123")
        self.assertEqual(len(accounts.data[0].tasks), 2)
        self.assertEqual(accounts.data[0].tasks[0], "task1")
        self.assertEqual(accounts.data[0].tasks[1], "task2")
        self.assertEqual(accounts.paging.cursors.before, "123")
        self.assertEqual(accounts.paging.cursors.after, "456")


class ExtendTokenTestCase(TestCase):
    def test_create_extend_token(self):
        access_token = "example_access_token"
        token_type = "example_token_type"
        expires_in = 3600

        extend_token = ExtendToken(access_token, token_type, expires_in)

        self.assertEqual(extend_token.access_token, access_token)
        self.assertEqual(extend_token.token_type, token_type)
        self.assertEqual(extend_token.expires_in, expires_in)

    def test_from_dict_method(self):
        data = {
            "access_token": "example_access_token",
            "token_type": "example_token_type",
            "expires_in": 3600,
        }

        extend_token = ExtendToken.from_dict(data)

        self.assertEqual(extend_token.access_token, data["access_token"])
        self.assertEqual(extend_token.token_type, data["token_type"])
        self.assertEqual(extend_token.expires_in, data["expires_in"])



class UserAuthTestCase(TestCase):
    def test_create_user_auth(self):
        access_token = "example_access_token"
        token_type = "example_token_type"

        user_auth = UserAuth(access_token, token_type)

        self.assertEqual(user_auth.access_token, access_token)
        self.assertEqual(user_auth.token_type, token_type)

    def test_from_dict_method(self):
        data = {
            "access_token": "example_access_token",
            "token_type": "example_token_type",
        }

        user_auth = UserAuth.from_dict(data)

        self.assertEqual(user_auth.access_token, data["access_token"])
        self.assertEqual(user_auth.token_type, data["token_type"])


class BasicProfileMetricsTestCase(TestCase):
    def test_create_basic_profile_metrics(self):
        data = {
            "id": "example_id",
            "username": "example_username",
            "media_count": 10,
            "followers_count": 100,
            "follows_count": 50,
            "name": "example_name",
            "biography": "example_biography",
            "profile_picture_url": "example_profile_picture_url",
        }

        profile_metrics = BasicProfileMetrics(**data)

        self.assertEqual(profile_metrics.id, data["id"])
        self.assertEqual(profile_metrics.username, data["username"])
        self.assertEqual(profile_metrics.media_count, data["media_count"])
        self.assertEqual(profile_metrics.followers_count, data["followers_count"])
        self.assertEqual(profile_metrics.follows_count, data["follows_count"])
        self.assertEqual(profile_metrics.name, data["name"])
        self.assertEqual(profile_metrics.biography, data["biography"])
        self.assertEqual(profile_metrics.profile_picture_url, data["profile_picture_url"])

    def test_from_dict_method(self):
        data = {
            "id": "example_id",
            "username": "example_username",
            "media_count": 10,
            "followers_count": 100,
            "follows_count": 50,
            "name": "example_name",
            "biography": "example_biography",
            "profile_picture_url": "example_profile_picture_url",
        }

        profile_metrics = BasicProfileMetrics.from_dict(data)

        self.assertEqual(profile_metrics.id, data["id"])
        self.assertEqual(profile_metrics.username, data["username"])
        self.assertEqual(profile_metrics.media_count, data["media_count"])
        self.assertEqual(profile_metrics.followers_count, data["followers_count"])
        self.assertEqual(profile_metrics.follows_count, data["follows_count"])
        self.assertEqual(profile_metrics.name, data["name"])
        self.assertEqual(profile_metrics.biography, data["biography"])
        self.assertEqual(profile_metrics.profile_picture_url, data["profile_picture_url"])


class PostInfoTestCase(TestCase):
    def test_create_post_info(self):
        data = {
            "like_count": 50,
            "media_url": "example_media_url",
            "permalink": "example_permalink",
            "timestamp": "2023-01-01T12:00:00",
            "caption": "example_caption",
            "comments_count": 10,
            "media_type": "image",
            "id": "example_id",
        }

        post_info = PostInfo(**data)

        self.assertEqual(post_info.like_count, data["like_count"])
        self.assertEqual(post_info.media_url, data["media_url"])
        self.assertEqual(post_info.permalink, data["permalink"])
        self.assertEqual(post_info.timestamp, data["timestamp"])
        self.assertEqual(post_info.caption, data["caption"])
        self.assertEqual(post_info.comments_count, data["comments_count"])
        self.assertEqual(post_info.media_type, data["media_type"])
        self.assertEqual(post_info.id, data["id"])

    def test_from_dict_method(self):
        data = {
            "like_count": 50,
            "media_url": "example_media_url",
            "permalink": "example_permalink",
            "timestamp": "2023-01-01T12:00:00",
            "caption": "example_caption",
            "comments_count": 10,
            "media_type": "image",
            "id": "example_id",
        }

        post_info = PostInfo.from_dict(data)

        self.assertEqual(post_info.like_count, data["like_count"])
        self.assertEqual(post_info.media_url, data["media_url"])
        self.assertEqual(post_info.permalink, data["permalink"])
        self.assertEqual(post_info.timestamp, data["timestamp"])
        self.assertEqual(post_info.caption, data["caption"])
        self.assertEqual(post_info.comments_count, data["comments_count"])
        self.assertEqual(post_info.media_type, data["media_type"])
        self.assertEqual(post_info.id, data["id"])