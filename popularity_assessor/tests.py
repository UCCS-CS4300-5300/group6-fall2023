from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

from popularity_assessor.models import InstagramAccount
from popularity_assessor.views import delete_account, get_followers, get_likes
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
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
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
            reverse('popularity_assessor:profile', args=['testuser'])
        )
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
        self.user = User.objects.create_user(
            username='test', password='test_pass'
        )
        self.ig_account = InstagramAccount(user=self.user, token='test')
        self.ig_account.save()
        self.creds = {'username': 'test', 'password': 'test_pass'}

    def test_delete_account_request(self):
        """
        Test the functionality of the account deletion process.
        """
        self.client.login(**self.creds)
        response = self.client.post(
            reverse('popularity_assessor:profile', args=(self.creds['username'],)),
            follow=True
        )
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
        self.user = User.objects.create_user(
            self.username, 'test@example.com', self.password
        )

    def test_user_account_lifecycle(self):
        """
        Test registration, login, and logout functionalities.
        """
        # Test registration
        response = self.client.post(reverse('popularity_assessor:register'), {
            'username': 'newuser', 'password1': 'newpassword123', 'password2': 'newpassword123'
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

        # Test login
        self.client.login(username='newuser', password='newpassword123')
        self.assertTrue('_auth_user_id' in self.client.session)

        # Test logout
        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)


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
