from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import InstagramAccount
from .helpers import get_password_validators_help_texts
from .decorators import facebook_auth_check
from facebook_api.helpers.get_accessToken import GetAccessToken
from datetime import datetime, timedelta  # for mock data
import random


def connectInsta(request):
    code = request.GET.get('code')
    user_auth = GetAccessToken().user(code, request.get_host() + request.path)

    # create a new instagram account in the DB
    account = InstagramAccount(user=request.user, token=user_auth.access_token)
    account.save()

    return redirect('popularity_assessor:profile',
                    user_name=request.user.username)


# This function will be used to get all of the user's posts and post metadata
def get_posts(self):
    posts = [{
        'title': 'Beach Rocks',
        'img_path': 'src/post_sample_1.jpg',
        'num_comments': 4,
        'date': 'September 9, 2023',
        'likes': 30,
    }, {
        'title': 'New Beginning',
        'img_path': 'src/post_sample_2.jpg',
        'num_comments': 9,
        'date': 'November 6, 2021',
        'likes': 50,
    }, {
        'title': 'Snowy Owl',
        'img_path': 'src/post_sample_3.jpg',
        'num_comments': 10,
        'date': 'November 11, 2022',
        'likes': 60,
    }]

    return posts


def delete_account(user=None):
    if user is not None:
        user.delete()
    else:
        raise User.DoesNotExist


@login_required
@facebook_auth_check
def profile(request, user_name):
    # For now, the only POST request is used to delete account.
    # In the future, this must be checked further to very what the user want. (ex: delete vs. manage metrics
    if request.method == "POST":
        user_to_delete = request.user
        delete_account(user_to_delete)
        return redirect('popularity_assessor:login')

    # Use the new mock functions
    user_metrics = mock_user_metrics()
    posts = mock_posts()

    # Format the dates for today and yesterday
    # Get the current date and time
    now = datetime.now()

    # Calculate the date for yesterday
    yesterday = now - timedelta(days=2)

    # Format the date as MM/DD
    yesterday_formatted = yesterday.strftime("%m/%d")
    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
  
    # Calculate likes from today and yesterday
    '''
    likes_today = sum(
        len([
            like for like in post['likes']
            if like['timestamp'].startswith(today_str)
        ]) for post in posts)

    '''
    posts2 = get_posts(None)
    likes_today = 0
    for post in posts2:
      likes_today += post['likes']

    likes_yesterday = sum(
        len([
            like for like in post['likes']
            if like['timestamp'].startswith(yesterday_str)
        ]) for post in posts)
    
    metrics  = request.api.general.get_profile_metrics()
    posts = request.api.general.get_posts()

    # get the first 10 posts if there is less than 10 posts just get all of them
    if len(posts.data) < 5:
        posts = posts.data
    else:
        posts = posts.data[0:5]

    posts_data = []
    for post in posts:
        posts_data.append(request.api.general.get_post_data(post.id))
    

    # Pass data to the template
    return render(
        request, 'profile.html', {
            "posts": get_posts(None),
            "user_metrics": user_metrics,
            "likes_today": likes_today,
            "likes_yesterday": likes_yesterday,
            "yesterday_date": yesterday_formatted,
            "profile_metrics": metrics
        })


def register(request):
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

    password_help_texts = get_password_validators_help_texts()
    context = {'form': form, 'password_help_texts': password_help_texts}
    return render(request, 'register.html', context)


def custom_login(request):
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


def mock_user_metrics():
    # Mocking user metrics until API is fully implemented
    username = "John Doe"
    current_followers = 310
    followers_yesterday = 320
    total_posts = 100
    following = 207

    return {
        'total_posts': total_posts,
        'current_followers': current_followers,
        'followers_yesterday': followers_yesterday,
        'following': following,
        'username': username,
    }


def mock_posts():
    posts = []

    for i in range(1, 6):
        post_date = datetime.now() - timedelta(days=random.randint(0, 4))
        num_likes = random.randint(10,
                                   100)  # Random number of likes for the post
        likes = []

        for _ in range(num_likes):
            # Generate a random timestamp for each like between the post_date and now
            like_timestamp = post_date + timedelta(seconds=random.randint(
                0, int((datetime.now() - post_date).total_seconds())))
            likes.append(
                {'timestamp': like_timestamp.strftime("%Y-%m-%d %H:%M:%S")})

        posts.append({
            'image_path': f'path/to/image{i}.jpg',
            'title': f'Post {i}',
            'date': post_date.strftime("%Y-%m-%d"),
            'likes': likes,
            'num_comments': random.randint(2, 10)
        })

    return posts
