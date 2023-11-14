from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect
from .models import InstagramAccount
from urllib.parse import urlencode
import random
import os
from functools import wraps

def facebook_auth_check(view_func):
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        try:
            user = request.user

            # Check if the user's account is connected with an Instagram account
            IGAcc = InstagramAccount.objects.get(pk=user.id)

            # TODO: Implement access code expiration check
            # TODO: Add access code to request body for use in view

        except InstagramAccount.DoesNotExist:
            # Generate a random number for CSRF protection
            RANDOM_NUMBER = random.randrange(100000000, 999999999)

            # Retrieve the Facebook client ID from the environment variable
            client_id = os.getenv("FB_CLIENT_ID")
            if client_id is None:
                raise ValueError("Facebook client id environment variable not set")

            # Generate the redirect URL for Facebook authentication
            params = {
                "client_id": client_id,
                "redirect_uri": request.build_absolute_uri(reverse("popularity_assessor:connect-insta")),
                "response_type": "code",
                "state": RANDOM_NUMBER
            }

            fb_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
            return redirect(fb_auth_url)

        # Continue to the original view
        return view_func(request, *args, **kwargs)

    return wrapped_view