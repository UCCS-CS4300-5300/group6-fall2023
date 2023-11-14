from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

### NOTE
# https://django-cryptography.readthedocs.io/en/latest/installation.html
# pip install django-cryptography
# this is used for the encryption of the token so that we can get the token from the database


# Create your models here.
class InstagramAccount(models.Model):
    """
    This is the model for the instagram account,
    Will be used to track the popularity of the user
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )  # user that owns this account, this is cascaded so that if the user is deleted, the account is deleted
    token = encrypt(
        models.CharField(max_length=255, default=None)
    )  # token for this account on instagram)
    previous_likes = models.IntegerField(default=0)  # previous likes on the last post
    previous_followers = models.IntegerField(
        default=0
    )  # previous followers on the last post
    previous_date = models.DateTimeField(
        auto_now_add=True
    )  # previous date of the last post

    def get_token(self):
        """
        Get the token for this account
        """
        return self.token
