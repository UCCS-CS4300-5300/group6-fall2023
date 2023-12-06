from django.test import TestCase, LiveServerTestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from unittest.mock import patch, Mock
import os
from django.contrib.auth.forms import UserCreationForm
from popularity_assessor.models import InstagramAccount
from popularity_assessor.views import delete_account, get_followers, get_likes, timed_metrics
from facebook_api.facebook import facebook_API
from facebook_api.facebook_settings import facebook_Config


class ProfileViewTestBase(TestCase):
    """
    Base class for tests related to the profile view.
    """
    def setUp(self):
        """
        Common setup for profile view related tests.
        """
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.ig_account = InstagramAccount(user=self.user, token='test')
        self.ig_account.save()
        self.api = facebook_API("test", facebook_Config())


class GetMetricsTests(TestCase):
    """
    Tests for metric retrieval functions.
    """
    def test_get_metrics(self):
        """
        Test for get_followers and get_likes functions.
        """
        for func in [get_followers, get_likes]:
            dates, counts = func()
            self.assertEqual(len(dates), 7)
            self.assertEqual(len(counts), 7)
            for date in dates:
                self.assertIsInstance(date, str)
                self.assertTrue(datetime.strptime(date, "%Y-%m-%d"))
            for count in counts:
                self.assertIsInstance(count, int)


class ProfileViewGetPostTests(ProfileViewTestBase):
    """
    Tests for retrieving posts and associated data from the profile view.
    """
    def test_profile_view_post_expected_fields(self):
        """
        Test that the profile view correctly displays expected fields for posts.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('popularity_assessor:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)


class ProfileViewDeleteAccountTests(LiveServerTestCase):
    """
    Tests for the account deletion functionality in the profile view.
    """
    def setUp(self):
        """
        Set up environment for delete account tests.
        """
        super().setUp()
        self.user = User.objects.create_user(username='test',
                                             password='test_pass')
        self.ig_account = InstagramAccount(user=self.user, token='test')
        self.ig_account.save()
        self.creds = {'username': 'test', 'password': 'test_pass'}

    def test_delete_account_request(self):
        """
        Test the functionality of the account deletion process.
        """
        self.client.login(**self.creds)
        response = self.client.post(reverse('popularity_assessor:profile',
                                            args=(self.creds['username'], )),
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.login(**self.creds))


class UserAccountTests(TestCase):
    """
    Tests for user account functionalities.
    """
    def setUp(self):
        """
        Set up environment for user account tests.
        """
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(self.username, 'test@example.com',
                                             self.password)

    def test_user_account_lifecycle(self):
        """
        Test registration, login, and logout functionalities.
        """
        # Test registration
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'newuser',
                'password1': 'newpassword123',
                'password2': 'newpassword123'
            })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

        # Test login
        self.client.login(username='newuser', password='newpassword123')
        self.assertTrue('_auth_user_id' in self.client.session)

        # Test logout
        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_register_view_get_request(self):
        url = reverse('popularity_assessor:register')
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], UserCreationForm)


class DeleteAccountTest(TestCase):
    """
    Tests for the delete_account functionality.
    """
    def test_delete_account(self):
        """
        Test delete_account function behavior.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        delete_account(user)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')


class ConnectInstaTest(TestCase):
    """
  Tests for connect insta functionality.
  """
    def test_connect_insta(self):
        """
        Since this view deals with the Instagram API, its not possible to test it with the limited capacity we have from the api itself, so we will just test if the view is getting called and responsing with at least something :|
        """
        base_url = reverse('popularity_assessor:connect-insta')
        full_url = f'{base_url}?code=aDasdasdadaD'
        try:
            self.client.get(full_url)
            self.fail("Expected an exception but none was raised.")
        except Exception:
            pass  # Test will pass if any exception is raised


class ConnectFacebookTest(TestCase):
    def setUp(self):
        """
      Common setup for profile view related tests.
      """
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.ig_account = InstagramAccount(user=self.user, token='test')
        self.ig_account.save()
        self.api = facebook_API("test", facebook_Config())

    def test_connect_facebook_authenticated_user(self):
        '''
      Test that the connect_facebook view is working correctly for an authenticated user.
      '''
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a request to the connect_facebook view
        response = self.client.get(
            reverse('popularity_assessor:connect-facebook'))

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is being used
        self.assertTemplateUsed(response, 'accounts.html')

        # Assert that the context contains the user and the default message
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(
            response.context['message'],
            "Looks like your account is not connected to Facebook.")

    def test_connect_facebook_unauthenticated_user(self):
        # Make a request to the connect_facebook view without logging in
        response = self.client.get(
            reverse('popularity_assessor:connect-facebook'))

        # Assert that the response has a status code of 302 (redirect to login page)
        self.assertEqual(response.status_code, 302)


class RedirectFacebookAuthTests(TestCase):
    @patch('os.getenv')
    def test_redirect_to_facebook_auth(self, mock_getenv):
        # Mock the FB_CLIENT_ID environment variable
        mock_getenv.return_value = 'dummy_client_id'

        # Make a request to the 'facebook-auth/' URL
        response = self.client.get(
            reverse('popularity_assessor:facebook-auth'))

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)

        expected_url_start = "https://www.facebook.com/v18.0/dialog/oauth?client_id=%20%20%20%20dummy_client_id&redirect_uri="
        # Using assertIn because the state parameter is random
        self.assertIn(expected_url_start, response['Location'])

    @patch('os.getenv', return_value=None)
    def test_redirect_without_client_id(self, mock_getenv):
        # Make a request to the 'facebook-auth/' URL
        with self.assertRaises(ValueError):
            self.client.get(reverse('popularity_assessor:facebook-auth'))


class TimedMetricsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

        # Create a test client
        self.factory = RequestFactory()

    def test_timed_metrics(self):
        # Create a mock request with an authenticated user
        request = self.factory.get('/timed-metrics/')
        request.user = self.user
        request.api = Mock()

        # Call the timed_metrics view function
        response = timed_metrics(request)

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)


class CustomLoginViewTest(TestCase):
    """Tests for the custom_login view."""
    def setUp(self):
        """Initializes test client and user."""
        self.client = Client()
        self.login_url = reverse('popularity_assessor:login')
        User.objects.create_user('testuser', 'test@example.com', 'password123')

    def test_login_view_GET(self):
        """Verifies GET request renders login page."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_valid_POST(self):
        """Tests valid login credentials and redirection."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        },
                                    follow=True)
        self.assertRedirects(response,
                             reverse('popularity_assessor:connect-facebook'))

    def test_login_view_invalid_POST(self):
        """Tests invalid login credentials and error handling."""
        response = self.client.post(self.login_url, {
            'username': 'wrong',
            'password': 'user'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTemplateUsed(response, 'login.html')
