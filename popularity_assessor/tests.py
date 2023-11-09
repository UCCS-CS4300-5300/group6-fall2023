from django.test import TestCase 
from django.contrib.auth.models import User
from popularity_assessor.views import delete_account


# Create your tests here.

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