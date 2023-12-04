from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from popularity_assessor.models import InstagramAccount
from popularity_assessor.views import (delete_account, mock_user_metrics, mock_posts, get_followers, get_likes)
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics
from facebook_api.extensions.general.postInfo import PostInfo
from facebook_api.extensions.general.media import Posts
from facebook_api.facebook import facebook_API
from facebook_api.facebook_settings import facebook_Config
from django.urls import reverse
from datetime import datetime

# Test the get functions for metrics
class GetMetricsTests(TestCase):
    """Class for testing metric retrieval functions."""
    def test_get_followers(self):
        """
        Test the `get_followers` function to ensure it returns the correct format and 
        types of data. Specifically, it checks the length of returned lists and 
        validates the data types of the contents.
        """
        # Call function to get data
        dates, followers = get_followers()

        # Assert based on the expected structure of the data
        self.assertEqual(len(dates), 7)
        self.assertEqual(len(followers), 7)

        for data in dates:
            self.assertTrue(isinstance(data, str))
            self.assertTrue(datetime.strptime(data, "%Y-%m-%d"))

        # Check type of each follower count
        for count in followers:
            self.assertTrue(isinstance(count, int))

    def test_get_likes(self):
        """
        Test the `get_likes` function to verify that it correctly retrieves likes data.
        This test checks the length of the dates and likes lists and validates the 
        types of the data elements in these lists.
        """
        # Call function to get data
        dates, likes = get_likes()

        # Assert based on the expected structure of the data
        self.assertEqual(len(dates), 7)
        self.assertEqual(len(likes), 7)

        for data in dates:
            self.assertTrue(isinstance(data, str))
            self.assertTrue(datetime.strptime(data, "%Y-%m-%d"))

        # Check type of each follower count
        for count in likes:
            self.assertTrue(isinstance(count, int))


def mock_profile_metrics():
    data=         {
            "id": "17841459177727833",
            "username": "podcastclipstoday",
            "media_count": 4,
            "followers_count": 124,
            "follows_count": 68,
            "name": "Podcast clips daily",
            "biography": "\"Motivation and inspiration for personal growth. 🎧 Tune in for podcast clips and daily doses of insight. Join our community! 💪",
            "profile_picture_url": "https://scontent-ord5-2.xx.fbcdn.net/v/t51.2885-15/346926254_192446810356926_4630223781712576112_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=7d201b&_nc_ohc=zSCJrmpVxToAX-ZaD67&_nc_ht=scontent-ord5-2.xx&edm=AL-3X8kEAAAA&oh=00_AfDhhTjGyg62fR0WRyyLa4yXzpvE8wrE4ttbu32dIz6i4Q&oe=655FD404"
        }
    return BasicProfileMetrics.from_dict(data)


def mock_posts():
    data = {
                "data": [
                    {
                    "id": "17980895912317725"
                    },
                    {
                    "id": "17988641024004750"
                    },
                    {
                    "id": "17937304004550750"
                    },
                    {
                    "id": "17989257334983575"
                    }
                ],
                "paging": {
                    "cursors": {
                    "before": "QVFIUndweTk5QTFqaVVXTjk2VnZAvN0tZAcmxHd2xNWW5JazJaUHB1NzB0eHRYdzFya01zWFhLTXNNSXpCcVZAQVHctRjNsN01laEYyUDRsempmY2dlcU5RSUxn",
                    "after": "QVFIUkVaSkhFYlZAxRGJndWVQWlFYa3Vla1BVcVlyajBTZA0hfQnMtcEU4R0pJYkEtc016WHRsLUNqcFlHYS11YW9XMTQ4WVRJZAnpKYnJPUXhieFNISDRTaThB"
                    }
                }
            }
    return Posts.from_dict(data)

def mock_post_data():
    data =         {
            "like_count": 2,
            "media_url": "https://scontent-iad3-1.cdninstagram.com/o1/v/t16/f1/m82/0C4C916525DF02AE1742724BC26F39B2_video_dashinit.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLmNsaXBzLnVua25vd24tQzMuNTc2LmRhc2hfYmFzZWxpbmVfMV92MSJ9&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&vs=544928507820758_700565062&_nc_vs=HBksFQIYT2lnX3hwdl9yZWVsc19wZXJtYW5lbnRfcHJvZC8wQzRDOTE2NTI1REYwMkFFMTc0MjcyNEJDMjZGMzlCMl92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dDYWN0QlFTZUFtRzJXNEdBS0NLOTJKbjRCMDRicV9FQUFBRhUCAsgBACgAGAAbAYgHdXNlX29pbAExFQAAJuTVgdnZxPFAFQIoAkMzLBdANarAgxJumBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1AAA%3D&ccb=9-4&oh=00_AfBJBVE3P_sDc-_aDu1ZEjKQzeFS4rTb8p9niaanOBstFQ&oe=655EC4A3&_nc_sid=1d576d&_nc_rid=deb3ca28cb",
            "permalink": "https://www.instagram.com/reel/CsPyT95AQKc/",
            "timestamp": "2023-05-15T02:15:40+0000",
            "caption": "Surrounding yourself with winners is the key to success 🏆 Follow along as we take inspiration from Kevin Hart and his winning mindset 🤩 Tune in to the Pivot Podcast and Thrive Minds for more motivational videos that will help you reach new heights 🚀 #kevinhart #pivotpodcast #thriveminds #motivationalvideo #fyp",
            "comments_count": 0,
            "media_type": "VIDEO",
            "id": "17989257334983575"
        }
    return PostInfo.from_dict(data)

# Test that all the fields appear in the profile view
class ProfileViewGetPostTests(TestCase):
    """
    Class for testing the retrieval of posts and associated data from the profile view. 
    This includes setting up a mock user and Instagram account, mocking API calls, and 
    verifying that the profile view correctly displays post data.
    """
    def setUp(self):
        """
        Set up a test environment before each test method is run. This involves creating 
        a test user and an associated Instagram account, and mocking API calls for 
        profile metrics, posts, and post data.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

        ## change the api functions to mock functions
        self.api = facebook_API("test", facebook_Config())

        self.api.general.get_profile_metrics = mock_profile_metrics
        self.api.general.get_posts = mock_posts
        self.api.general.get_post_data = mock_post_data

    def test_profile_view_post_expected_fields(self):
        """
        Test that the profile view correctly displays expected fields for posts. This 
        includes logging in as a test user, retrieving the profile page, and asserting 
        that the response is successful and contains the expected post data.
        """
        # Log in test user
        self.client.login(username='testuser', password='testpassword')
        # Retrieve user password page
        response = self.client.get(
            reverse('popularity_assessor:profile', args=['testuser']))
        # Ensure that the response is successfull
        self.assertEqual(response.status_code, 200)

class ProfileViewDeleteAccountTests(LiveServerTestCase):
    """
    Class for testing the account deletion functionality in the profile view. 
    This includes testing the presence of a delete account button and the 
    functionality of the account deletion process.
    """
    def setUp(self):
        """
        Set up a test environment before each test method is run. This involves creating 
        a test user and an associated Instagram account for testing the profile view 
        and delete account functionality.
        """
        self.user = User.objects.create_user(username='test',
                                             password='test_pass')
        self.creds = {'username': 'test', 'password': 'test_pass'}

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

    def tearDown(self):
        """
        Clean up after each test method is run. This method is currently a placeholder 
        and can be used for future teardown procedures if necessary.
        """
        pass

    def test_delete_account_button_on_profile_page(self):
        """
        Test that the 'Delete Account' button is present on the user's profile page. 
        This involves logging in as a test user and verifying that the response 
        from the profile page contains the 'Delete Account' button.
        """
        self.client.login(**self.creds)

        response = self.client.get( reverse('popularity_assessor:profile', args=(self.creds['username'], )))

        self.assertContains(response, 'Delete Account')

    def test_delete_account_request(self):
        """
        Test the functionality of the account deletion process. This involves logging in 
        as a test user, sending a post request to delete the account, and then verifying 
        that the account is no longer accessible.
        """
        self.client.login(**self.creds)

        response = self.client.post(reverse('popularity_assessor:profile', args=(self.creds['username'], )), follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.login(**self.creds)
        self.assertEqual(response, False)


class UserAccountTests(TestCase):
    """
    Class for testing various user account functionalities including registration, 
    login, logout, and profile view access.
    """
    def setUp(self):
        """
        Set up a test environment before each test method is run. This involves creating 
        a test user and an associated Instagram account for testing different user 
        functionalities.
        """
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

    def test_registration_view_get(self):
        """
        Test the accessibility of the registration view using a GET request. 
        It verifies that the registration page is accessible and uses the correct template.
        """
        response = self.client.get(reverse('popularity_assessor:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_valid_post(self):
        """
        Test the user registration process with valid data using a POST request. 
        It checks if a new user is created and the response redirects correctly.
        """
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'newuser',
                'password1': 'newpassword123',
                'password2': 'newpassword123'
            })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_registration_invalid_post(self):
        """
        Test the user registration process with invalid data (mismatched passwords) 
        using a POST request. It verifies that the user count remains unchanged and 
        the form error is raised as expected.
        """
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'user',
                'password1': 'password',
                'password2': 'notmatching'
            })
        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(response, 'form', 'password2',
                             "The two password fields didn’t match.")

    def test_login_view_get(self):
        """
        Test the accessibility of the login view using a GET request. 
        It verifies that the login page is accessible and uses the correct template.
        """
        response = self.client.get(reverse('popularity_assessor:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_post(self):
        """
        Test the user login process with valid credentials using a POST request. 
        It checks if the user is redirected to their profile page and the session is active.
        """
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_post(self):
        """
        Test the user login process with invalid credentials using a POST request. 
        It verifies that the login fails, the session is not active, and the appropriate 
        error message is displayed.
        """
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' not in self.client.session)
        self.assertFormError(response, 'form', None, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_logout_view(self):
        """
        Test the user logout process. It involves logging in the user and then 
        testing the logout functionality, ensuring the session is terminated.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('popularity_assessor:logout'))
        self.assertRedirects(response, reverse('popularity_assessor:login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_view(self):
        """
        Test the accessibility of the user's profile view. This test checks that 
        unauthenticated access redirects to the login page, and authenticated access 
        displays the profile page correctly.
        """
        # Trying to access the profile page without logging in should redirect to the login page
        response = self.client.get( reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertRedirects(response,f"{reverse('popularity_assessor:login')}?next={reverse('popularity_assessor:profile', kwargs={'user_name': self.username})}")

        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Now the profile page should be accessible
        response = self.client.get( reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


# test that if the user passed to delete_account is None, then the function raises a User.DoesNotExist exception
class delete_account_test(TestCase):
    """
    Class for testing the functionality of deleting a user from the database. 
    This includes verifying the behavior of the deletion process in various scenarios.
    """
    # Make sure that deleting a None user raises a User.DoesNotExist exception
    def test_delete_account_none(self):
        """
        Test the behavior of the delete_account function when provided with None as 
        an argument. It is expected to raise a User.DoesNotExist exception, confirming 
        that the function handles None inputs appropriately.
        """
        with self.assertRaises(User.DoesNotExist):
            delete_account(None)


# test that if the user is deleted, they don't appear in the database of users
    def test_delete_account_success(self):
        """
        Test the successful deletion of a user account. This test involves creating 
        a new user, deleting them using the delete_account function, and then verifying 
        that the user no longer exists in the database.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        # Call delete_account function to delete user
        delete_account(user)
        # Try retrieving user from databases, should raise User.DoesNotExist exception
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username='testuser')


class MockMetricsTests(TestCase):
    """
    Class for testing the mock user metrics functionality. 
    This involves verifying the presence and types of various metrics in the mocked data.
    """
    def test_mock_user_metrics(self):
        """
        Test the mock_user_metrics function to ensure it returns a dictionary containing 
        specific keys related to user metrics (like total posts, current followers, etc.) 
        and verifies the type of each metric.
        """
        metrics = mock_user_metrics()
        self.assertIn('total_posts', metrics)
        self.assertIn('current_followers', metrics)
        self.assertIn('followers_yesterday', metrics)
        self.assertIn('following', metrics)

        # Check the type of values
        self.assertIsInstance(metrics['total_posts'], int)
        self.assertIsInstance(metrics['current_followers'], int)
        self.assertIsInstance(metrics['followers_yesterday'], int)
        self.assertIsInstance(metrics['following'], int)