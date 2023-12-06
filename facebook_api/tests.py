'''
Test for the facebook api
'''


from django.test import TestCase # pylint: disable=import-error, E0401

from facebook_api.extensions.error import RequestError
from facebook_api.extensions.general.me import Me
from facebook_api.extensions.general.businessAccounts import BusinessAccounts, InstagramBusinessAccount
from facebook_api.extensions.general.accounts import Accounts, CategoryList, Datum as DatumAccount
from facebook_api.extensions.general.media import Posts, Datum, Paging, Cursors
from facebook_api.extensions.authentication.extendToken import ExtendToken
from facebook_api.extensions.authentication.userAuth import UserAuth
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics
from facebook_api.extensions.general.postInfo import PostInfo
from facebook_api.facebook_settings import facebook_Config

from facebook_api.facebook import facebook_API


class FacebookAPITest(TestCase):
    '''
    Test our facebook api class
    '''
    def setUp(self): # pylint: disable=C0103
        '''
        setup our facebook api instance
        '''
        self.facebook_api = facebook_API("123", facebook_Config())

    def test_set_token(self):
        '''
        test to see if we can set the token
        '''
        token = "test"
        self.facebook_api.set_token(token)
        self.assertEqual(self.facebook_api.token, token)
        self.assertEqual(self.facebook_api.required_params,
                         {'access_token': token})

    def mock_get_me(self):
        '''
        get a mock me object
        '''
        return Me.from_dict({"name": "test", "id": "test"})

    def mock_get_accounts(self, endpoint, object_return_type):
        '''
        mock the get accounts method
        '''
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
                    "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxX"
                    + "HpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3",
                    "after":
                    "QVFIUlM0dTJlcHItSGV3NHdPaHdZAZATFvc2E3ZAEljM0FlbWZAQOGJCNlBicWxXU"
                    + "HpyclpfUEtnaE5CeC1XWFpVS18zamRNOUtVSXdyR0VaOXZAnV0xtZAkd3eXJ3"
                }
            }
        })
    
    def mock_business_accounts(self):
        '''
        mock the get business accounts method
        '''
        return BusinessAccounts.from_dict({
            "instagram_business_account": {
                "id": "123"
            },
            "id": "123"
        })

    def mock_get_posts(self):
        '''
        mock the get posts method
        '''
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
    
    # def mock_get_profile_metrics(self):
    #     '''
    #     mock the get profile metrics method
    #     '''
    #     return BasicProfileMetrics.from_dict({
    #         "id": "123",
    #         "username": "test",
    #         "media_count": 10,
    #         "followers_count": 100,
    #         "follows_count": 50,
    #         "name": "test",
    #         "biography": "test",
    #         "profile_picture_url": "https://example.com"
    #     })
    
    # def test_get_profile_metrics(self):
    #     '''
    #     test for getting profile metrics
    #     '''
    #     self.facebook_api.general.get_business_accounts = self.mock_business_accounts
    #     self.facebook_api.general.get = self.mock_get_profile_metrics
    #     resp = self.facebook_api.general.get_profile_metrics()

    #     self.assertIsInstance(resp, BasicProfileMetrics)
    #     self.assertEqual(resp.id, "123")


    def test_get_posts(self):
        '''
        test for getting posts
        '''
        self.facebook_api.general.get_posts = self.mock_get_posts
        resp = self.facebook_api.general.get_posts()
        self.assertIsInstance(resp, Posts)
        self.assertEqual(resp.data[0].id, "123")



    def test_get_accounts(self):
        '''
        test for getting accounts
        '''
        self.facebook_api.get = self.mock_get_accounts
        resp = self.facebook_api.general.get_accounts()
        self.assertIsInstance(resp, Accounts)
        self.assertEqual(resp.data[0].access_token, "1234")

    def test_fail_request_oauth(self):
        '''
        test for fail on request oauth
        used to make sure that they get a request error object
        '''
        resp = self.facebook_api.get("test", object_return_type=RequestError)
        self.assertIsInstance(resp, RequestError)
        self.assertEqual(resp.error.type, "OAuthException")


class FacebookMeTests(TestCase):
    '''
    Test our Me class
    '''
    def test_create_instance_with_valid_name_and_id(self):
        '''
        test to see if the instance is created with the
         correct name and id
        '''
        name = 'John'
        id = '123'
        me = Me(name, id)
        self.assertEqual(me.name, name)
        self.assertEqual(me.id, id)



    def test_from_dict(self):
        '''
        Test to see if we can create an instance
          of Me from a dictionary
        '''
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



class PostCursorsTestCase(TestCase):
    '''
    PostCursor test case for the facebook api
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Cursors
        '''
        cursors_dict = {"before": "123", "after": "456"}
        cursors = Cursors.from_dict(cursors_dict)
        self.assertEqual(cursors.before, "123")
        self.assertEqual(cursors.after, "456")


class PostDatumTestCase(TestCase):
    '''
    test for the datum part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Datum
        '''
        datum_dict = {"id": "789"}
        datum = Datum.from_dict(datum_dict)
        self.assertEqual(datum.id, "789")


class PostPagingTestCase(TestCase):
    '''
    test for the paging part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Paging
        '''
        paging_dict = {"cursors": {"before": "123", "after": "456"}}
        paging = Paging.from_dict(paging_dict)
        self.assertEqual(paging.cursors.before, "123")
        self.assertEqual(paging.cursors.after, "456")


class PostPostsTestCase(TestCase):
    '''
    test for the posts part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Posts
        '''
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


class InstaAccountsInstagramBusinessAccountTestCase(TestCase):
    '''
    test for the instagram business account part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of InstagramBusinessAccount
        '''
        data = {"id": "123"}
        instagram_business_account = InstagramBusinessAccount.from_dict(data)
        self.assertEqual(instagram_business_account.id, "123")


class InstaAccountsBusinessAccountsTestCase(TestCase):
    '''
    test for the business accounts part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of BusinessAccounts
        '''
        data = {
            "instagram_business_account": {"id": "456"},
            "id": "789"
        }
        business_accounts = BusinessAccounts.from_dict(data)
        self.assertEqual(business_accounts.id, "789")
        self.assertEqual(
            business_accounts.instagram_business_account.id, "456")


class AccountCategoryListTestCase(TestCase):
    '''
    test for the category list part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of CategoryList
        '''
        data = {"id": "1", "name": "Category1"}
        category_list = CategoryList.from_dict(data)
        self.assertEqual(category_list.id, "1")
        self.assertEqual(category_list.name, "Category1")


class AccountCursorsTestCase(TestCase):
    '''
    test for the cursors part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Cursors
        '''
        data = {"before": "123", "after": "456"}
        cursors = Cursors.from_dict(data)
        self.assertEqual(cursors.before, "123")
        self.assertEqual(cursors.after, "456")


class AccountDatumTestCase(TestCase):
    '''
    test for the datum part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Datum for Accounts
        '''
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


class AccountPagingTestCase(TestCase):
    '''
    test for the paging part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Paging for Accounts
        '''
        data = {"cursors": {"before": "123", "after": "456"}}
        paging = Paging.from_dict(data)
        self.assertEqual(paging.cursors.before, "123")
        self.assertEqual(paging.cursors.after, "456")


class AccountAccountsTestCase(TestCase):
    '''
    test for the accounts part of the return for post
    '''
    def test_from_dict(self):
        '''
        test to see if we can create an instance of Accounts
        '''
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
    '''
    test for the extend token part of the return for post
    '''
    def test_create_extend_token(self):
        '''
        test to see if we can create an instance of ExtendToken
        '''
        access_token = "example_access_token"
        token_type = "example_token_type"
        expires_in = 3600

        extend_token = ExtendToken(access_token, token_type, expires_in)

        self.assertEqual(extend_token.access_token, access_token)
        self.assertEqual(extend_token.token_type, token_type)
        self.assertEqual(extend_token.expires_in, expires_in)

    def test_from_dict_method(self):
        '''
        test to see if we can create an instance of ExtendToken from a dictionary
        '''
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
    '''
    test for the user auth part of the return for post
    '''
    def test_create_user_auth(self):
        '''
        test to see if we can create an instance of UserAuth
        '''
        access_token = "example_access_token"
        token_type = "example_token_type"

        user_auth = UserAuth(access_token, token_type)

        self.assertEqual(user_auth.access_token, access_token)
        self.assertEqual(user_auth.token_type, token_type)

    def test_from_dict_method(self):
        '''
        test to see if we can create an instance of UserAuth from a dictionary
        '''
        data = {
            "access_token": "example_access_token",
            "token_type": "example_token_type",
        }

        user_auth = UserAuth.from_dict(data)

        self.assertEqual(user_auth.access_token, data["access_token"])
        self.assertEqual(user_auth.token_type, data["token_type"])


class BasicProfileMetricsTestCase(TestCase):
    '''
    tests for the basic profile metrics part of the return for post
    '''
    def test_create_basic_profile_metrics(self):
        '''
        test to see if we can create an instance of BasicProfileMetrics
        '''
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
        self.assertEqual(profile_metrics.followers_count,
                         data["followers_count"])
        self.assertEqual(profile_metrics.follows_count, data["follows_count"])
        self.assertEqual(profile_metrics.name, data["name"])
        self.assertEqual(profile_metrics.biography, data["biography"])
        self.assertEqual(profile_metrics.profile_picture_url,
                         data["profile_picture_url"])

    def test_from_dict_method(self):
        '''
        test to see if we can create an instance of BasicProfileMetrics from a dictionary
        '''
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
        self.assertEqual(profile_metrics.followers_count,
                         data["followers_count"])
        self.assertEqual(profile_metrics.follows_count, data["follows_count"])
        self.assertEqual(profile_metrics.name, data["name"])
        self.assertEqual(profile_metrics.biography, data["biography"])
        self.assertEqual(profile_metrics.profile_picture_url,
                         data["profile_picture_url"])


class PostInfoTestCase(TestCase):
    '''
    tests for the post info part of the return for post
    '''
    def test_create_post_info(self):
        '''
        test to see if we can create an instance of PostInfo
        '''
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
        '''
        test to see if we can create an instance of PostInfo from a dictionary
        '''
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
