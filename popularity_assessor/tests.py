"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTestCase(TestCase):
  def setUp(self):
    self.username = 'testuser'
    self.password = 'strongpassword123'
    User.objects.create_user(self.username, password=self.password)

  def test_registration_view_get(self):
    response = self.client.get(reverse('popularity_assessor:register'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'register.html')

  def test_registration_valid_post(self):
    response = self.client.post(reverse('popularity_assessor:register'), {
        'username': 'newuser',
        'password1': 'Newpass123',
        'password2': 'Newpass123'
    })
    self.assertEqual(User.objects.count(), 2)
    self.assertEqual(response.status_code, 302) 

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
    self.assertEqual(response.status_code, 302)
    self.assertTrue('_auth_user_id' in self.client.session)

  def test_login_invalid_post(self):
    response = self.client.post(reverse('popularity_assessor:login'), {
        'username': self.username,
        'password': 'wrongpassword'
    })
    self.assertEqual(response.status_code, 200)
    self.assertTrue('_auth_user_id' not in self.client.session)
    self.assertFormError(response, 'form', None, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

  def test_logout(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get(reverse('popularity_assessor:logout'))
    self.assertEqual(response.status_code, 302)
    self.assertFalse('_auth_user_id' in self.client.session)"""

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client

class UserAccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)

    def test_register_view(self):
        response = self.client.get(reverse('popularity_assessor:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse('popularity_assessor:register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertRedirects(response, reverse('popularity_assessor:profile', kwargs={'user_name': 'newuser'}))

    def test_login_view(self):
        response = self.client.get(reverse('popularity_assessor:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))

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

    def test_logout_view(self):
        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Log out
        response = self.client.get(reverse('popularity_assessor:logout'))
        self.assertRedirects(response, reverse('popularity_assessor:login'))

        # After logout, the profile page should not be accessible
        response = self.client.get(reverse('popularity_assessor:profile', kwargs={'user_name': self.username}))
        self.assertNotEqual(response.status_code, 200)

