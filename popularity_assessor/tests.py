from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

class UserAccountTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        User.objects.create_user(self.username, 'test@example.com', self.password)

    def test_registration_view_get(self):
        response = self.client.get(reverse('popularity_assessor:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_valid_post(self):
        response = self.client.post(reverse('popularity_assessor:register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertRedirects(response, reverse('popularity_assessor:profile', kwargs={'user_name': 'newuser'}))

    def test_registration_invalid_post(self):
        response = self.client.post(reverse('popularity_assessor:register'), {
            'username': 'user',
            'password1': 'password',
            'password2': 'notmatching'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")

    def test_login_view_get(self):
        response = self.client.get(reverse('popularity_assessor:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' not in self.client.session)
        self.assertFormError(response, 'form', None, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('popularity_assessor:logout'))
        self.assertRedirects(response, reverse('popularity_assessor:login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_view(self):
        # Trying to access the profile page without logging in should redirect to the login page
        response = self.client.get(reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertRedirects(response, f"{reverse('popularity_assessor:login')}?next={reverse('popularity_assessor:profile', kwargs={'user_name': self.username})}")

        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Now the profile page should be accessible
        response = self.client.get(reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
