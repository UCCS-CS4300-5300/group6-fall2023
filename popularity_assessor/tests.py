from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from bs4 import BeautifulSoup
from selenium import webdriver

from chromedriver_py import binary_path

# Create your tests here.

# Akshat and Yulia tests

# Test that the delete account button shows up on the profile page
# test that if the delete account button is pressed, the confirmation modal appears with the cancel and confirm options
# test that if the confirm button is pressed, the user is redirected to the login page
# test that if the cancel button is pressed, the confirmation modal disappears


class profile_view_tests(TestCase):
    def test_delete_account_button_on_profile_page(self):

        User.objects.create_user(username='test', password='test_pass')

        creds = {'username': 'test', 'password': 'test_pass'}

        self.client.login(**creds)

        response = self.client.get(
            reverse('popularity_assessor:profile', args=(creds['username'], )))

        html = BeautifulSoup(response.content)
        print(html.prettify())

        # svc = webdriver.ChromeService(executable_path=binary_path)
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)

        driver.get('http://0.0.0.0:3000/popularity_assessor/profile/test')

        self.assertContains(response, 'Delete Account')
        # There is only 1 modal and if its class is this, then it is not currently visible
        self.assertContains(response, '')


# test that if the user passed to delete_account is None, then the function raises a User.DoesNotExist exception
# test that if the user is deleted, they don't appear in the database of users
