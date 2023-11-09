from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from popularity_assessor.views import delete_account
from django.urls import reverse
from selenium import webdriver
from bs4 import BeautifulSoup
from chromedriver_py import binary_path


class ConnectInstagramTests(TestCase):
    def test_connection_insta_correct(self):
        data = {"token": 'test'}
        response = self.client.post('/popularity_assessor/connect-insta/',
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})


class ProfileViewDeleteAccountTests(LiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test_pass')
        self.creds = {'username': 'test', 'password': 'test_pass'}

    def tearDown(self):
        pass

    def test_delete_account_button_on_profile_page(self):

        self.client.login(**self.creds)

        response = self.client.get(
            reverse('popularity_assessor:profile',
                    args=(self.creds['username'], )))

        self.assertContains(response, 'Delete Account')

    def test_delete_account_request(self):

        self.client.login(**self.creds)

        response = self.client.post(reverse('popularity_assessor:profile',
                                            args=(self.creds['username'], )),
                                    follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.login(**self.creds)
        self.assertEqual(response, False)


class UserAccountTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        User.objects.create_user(self.username, 'test@example.com',
                                 self.password)

    def test_registration_view_get(self):
        response = self.client.get(reverse('popularity_assessor:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_valid_post(self):
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'newuser',
                'password1': 'newpassword123',
                'password2': 'newpassword123'
            })
        self.assertEqual(User.objects.count(), 2)
        self.assertRedirects(
            response,
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': 'newuser'}))

    def test_registration_invalid_post(self):
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
        response = self.client.get(reverse('popularity_assessor:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(
            response,
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' not in self.client.session)
        self.assertFormError(
            response, 'form', None,
            "Please enter a correct username and password. Note that both fields may be case-sensitive."
        )

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('popularity_assessor:logout'))
        self.assertRedirects(response, reverse('popularity_assessor:login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_view(self):
        # Trying to access the profile page without logging in should redirect to the login page
        response = self.client.get(
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertRedirects(
            response,
            f"{reverse('popularity_assessor:login')}?next={reverse('popularity_assessor:profile', kwargs={'user_name': self.username})}"
        )

        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Now the profile page should be accessible
        response = self.client.get(
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


# test that if the user passed to delete_account is None, then the function raises a User.DoesNotExist exception
class delete_account_test(TestCase):
    # Make sure that deleting a None user raises a User.DoesNotExist exception
    def test_delete_account_none(self):
        with self.assertRaises(User.DoesNotExist):
            delete_account(None)


# test that if the user is deleted, they don't appear in the database of users

    def test_delete_account_success(self):
        user = User.objects.create_user(username='testuser', password='12345')
        # Call delete_account function to delete user
        delete_account(user)
        # Try retrieving user from databases, should raise User.DoesNotExist exception
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username='testuser')
