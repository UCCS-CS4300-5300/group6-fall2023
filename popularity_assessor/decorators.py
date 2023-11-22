from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect
from facebook_api.facebook import facebook_API
from facebook_api.facebook import facebook_Config

from .models import InstagramAccount
from urllib.parse import urlencode
import random
import os
from functools import wraps
from facebook_api.helpers.get_accessToken import GetAccessToken


def facebook_auth_check(view_func):
    @wraps(view_func)
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        try:
            user = request.user

            # Check if the user's account is connected with an Instagram account
            IGAcc = InstagramAccount.objects.get(pk=user.id)

            getAccessToken = GetAccessToken()

            # TODO: Implement access code expiration check
            adminAccessToken = getAccessToken.admin().access_token
            
            validity = getAccessToken.debug(IGAcc.token, adminAccessToken)

            if validity != 'valid':
                request.message = "Looks like your Facebook access token has expired. Please reconnect your account."
                redirect("popularity_assessor:connect-facebook")

            request.api = facebook_API(IGAcc.token, facebook_Config())
        except InstagramAccount.DoesNotExist:

            return redirect("popularity_assessor:connect-facebook")

        # Continue to the original view
        return view_func(request, *args, **kwargs)

    return wrapped_view
