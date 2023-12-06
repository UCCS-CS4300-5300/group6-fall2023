"""
Controller for popularity_assessor

Functions:
    get_likes() -> str list, int list
    get_followers() -> str list, int list
    connect_insta(request) -> redirect
    redirect_to_facebook_auth(request) -> redirect
    delete_account(user) -> None
    connect_facebook(request) -> render
    profile(request, user_name) -> render
    register(request) -> redirect
    custom_login(request) -> redirect
"""
from datetime import datetime, timedelta  # for mock data
import random
import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from .models import InstagramAccount
from .decorators import facebook_auth_check
from facebook_api.extensions.error import RequestError
from facebook_api.helpers.get_accessToken import GetAccessToken
from facebook_api.extensions.profile.profileViews import ProfileViews
from facebook_api.extensions.profile.profileFollows import ProfileFollows
from django.http import JsonResponse


def get_likes():
    '''
    Mock likes from Instagram for last seven days
    '''
    now = datetime.now() - timedelta(days=1)

    dates = [(now - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
    dates.reverse()
    likes = [random.randint(-10, 25) for i in range(7)]

    return dates, likes


def get_followers():
    '''
    Mock followers from Instagram for last seven days
    '''
    # get yesterday's date
    now = datetime.now() - timedelta(days=1)

    dates = [(now - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
    dates.reverse()
    likes = [random.randint(-10, 25) for i in range(7)]

    return dates, likes


def connect_insta(request):
    '''
    connect Instagram account to the app
    '''
    code = request.GET.get('code')

    user_auth = GetAccessToken().user(code, request.get_host() + request.path)
    if (type(user_auth) == RequestError):
        raise ("Error with facebook auth")

    # create a new instagram account in the DB
    account = InstagramAccount(user=request.user, token=user_auth.access_token)
    account.save()

    return redirect('popularity_assessor:profile',
                    user_name=request.user.username)


def redirect_to_facebook_auth(request):
    '''
    if user has not linked their facebook to the app, redirect to facebook auth
    '''
    rand_state = random.randrange(100000000, 999999999)
    client_id = os.getenv("FB_CLIENT_ID")
    if client_id is None:
        raise ValueError("Facebook client id environment variable not set")

    url = request.build_absolute_uri(
        reverse('popularity_assessor:connect-insta'))

    url = url.replace("http://", "https://")

    fb_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id=\
    {client_id}&redirect_uri={url}&response_type=code&state={rand_state}"

    return redirect(fb_auth_url)


def delete_account(user=None):
    '''
    deletes user account, raises DoesNotExist error if the user is not given
    '''
    if user is not None:
        user.delete()
    else:
        raise User.DoesNotExist


@login_required
def connect_facebook(request):
    '''
    connects user to facebook account
    '''

    message = "Looks like your account is not connected to Facebook."

    try:
        message = request.message
    except:
        pass

    return render(request, 'accounts.html', {
        "user": request.user,
        "message": message
    })


@login_required
@facebook_auth_check
def profile(request, user_name):
    # For now, the only POST request is used to delete account.
    # In the future, this must be checked further to very what the user want. (ex: delete vs. manage metrics
    if request.method == "POST":
        user_to_delete = request.user
        delete_account(user_to_delete)
        return redirect('popularity_assessor:login')

    # Calculate likes from today and yesterday
    posts_data = []
    metrics = None

    try:
        metrics = request.api.general.get_profile_metrics()
        posts_data = request.api.general.get_batch_post_data()
    except:
        pass

    dates, likes = get_likes()
    _, followers = get_followers()

    # Pass data to the template
    return render(
        request, 'profile.html', {
            "posts": posts_data,
            "week_dates": dates,
            "week_likes": likes,
            "week_followers": followers,
            "profile_metrics": metrics
        })


@login_required
@facebook_auth_check
def timed_metrics(request):
    data_views: ProfileViews = request.api.general.get_profile_views()

    views = [
        data_views.data[0].values[i].value
        for i in range(len(data_views.data[0].values))
    ]
    data_follows: ProfileFollows = request.api.general.get_profile_follows()
    follows = [
        data_follows.data[0].values[i].value
        for i in range(len(data_follows.data[0].values))
    ]
    return JsonResponse({"views": views, "follows": follows})


def register(request):
    '''
    registers a new user
    '''
    # Handle the POST request (form submission)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after registration and redirect to profile
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('popularity_assessor:profile',
                            user_name=new_user.username)
    # Handle the GET request (displaying the form)
    else:
        form = UserCreationForm()

    password_help_texts = password_validators_help_texts()
    context = {'form': form, 'password_help_texts': password_help_texts}
    return render(request, 'register.html', context)


def custom_login(request):
    '''
     Handle the GET request (displaying the form)
    '''
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('popularity_assessor:profile',
                            user_name=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
