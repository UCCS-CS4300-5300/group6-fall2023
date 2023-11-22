from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import InstagramAccount
from .helpers import get_password_validators_help_texts
from .decorators import facebook_auth_check
from facebook_api.extensions.error import RequestError
from facebook_api.helpers.get_accessToken import GetAccessToken
from datetime import datetime, timedelta  # for mock data
import random
import os
import json


def get_likes():

    now = datetime.now()

    dates = [(now - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
    dates.reverse()
    likes = [random.randint(-10, 25) for i in range(7)]

    return dates, likes


def get_followers():

    now = datetime.now()

    dates = [(now - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(7)]
    dates.reverse()
    likes = [random.randint(-10, 25) for i in range(7)]

    return dates, likes

def connectInsta(request):
    code = request.GET.get('code')
    user_auth = GetAccessToken().user(code, request.get_host() + request.path)

    # create a new instagram account in the DB
    account = InstagramAccount(user=request.user, token=user_auth.access_token)
    account.save()

    return redirect('popularity_assessor:profile',
                    user_name=request.user.username)


def redirectToFacebookAuth(request):
    RANDOM_NUMBER = random.randrange(100000000, 999999999)
    client_id = os.getenv("FB_CLIENT_ID")
    if client_id is None:
                raise ValueError(
                    "Facebook client id environment variable not set")
    
    url = request.build_absolute_uri(reverse('popularity_assessor:connect-insta'))

    fb_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={client_id}&redirect_uri={url}&response_type=code&state={RANDOM_NUMBER}"

    return redirect(fb_auth_url)


# This function will be used to get all of the user's posts and post metadata
def get_posts(self):
    posts = [{
        "like_count": 2,
        "media_url": "https://scontent-iad3-1.cdninstagram.com/o1/v/t16/f1/m82/0C4C916525DF02AE1742724BC26F39B2_video_dashinit.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLmNsaXBzLnVua25vd24tQzMuNTc2LmRhc2hfYmFzZWxpbmVfMV92MSJ9&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&vs=544928507820758_700565062&_nc_vs=HBksFQIYT2lnX3hwdl9yZWVsc19wZXJtYW5lbnRfcHJvZC8wQzRDOTE2NTI1REYwMkFFMTc0MjcyNEJDMjZGMzlCMl92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dDYWN0QlFTZUFtRzJXNEdBS0NLOTJKbjRCMDRicV9FQUFBRhUCAsgBACgAGAAbAYgHdXNlX29pbAExFQAAJuTVgdnZxPFAFQIoAkMzLBdANarAgxJumBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1AAA%3D&ccb=9-4&oh=00_AfBJBVE3P_sDc-_aDu1ZEjKQzeFS4rTb8p9niaanOBstFQ&oe=655EC4A3&_nc_sid=1d576d&_nc_rid=deb3ca28cb",
        "permalink": "https://www.instagram.com/reel/CsPyT95AQKc/",
        "timestamp": "2023-05-15T02:15:40+0000",
        "caption": "Surrounding yourself with winners is the key to success 🏆 Follow along as we take inspiration from Kevin Hart and his winning mindset 🤩 Tune in to the Pivot Podcast and Thrive Minds for more motivational videos that will help you reach new heights 🚀 #kevinhart #pivotpodcast #thriveminds #motivationalvideo #fyp",
        "comments_count": 0,
        "media_type": "VIDEO",
        "id": "17989257334983575"
    }]

    return posts


def delete_account(user=None):
    if user is not None:
        user.delete()
    else:
        raise User.DoesNotExist

@login_required
def connectFacebook(request):

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
#@facebook_auth_check
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
      likes_today += post['like_count']

    likes_yesterday = sum(
        len([
            like for like in post['like_count']
            if like['timestamp'].startswith(yesterday_str)
        ]) for post in posts)
    
    metrics  = request.api.general.get_profile_metrics()
    posts = request.api.general.get_posts()
    posts_data = []
    if (type(posts) != RequestError):


        # get the first 10 posts if there is less than 10 posts just get all of them
        if len(posts.data) < 5:
            posts = posts.data
        else:
            posts = posts.data[0:5]


        for post in posts:
            postData = request.api.general.get_post_data(post.id)
            if (type(postData) == RequestError or postData.media_type != "IMAGE"):
                continue

            # convert the time(2023-05-15T02:15:40+0000) into date only 
            postData.timestamp = postData.timestamp.split('T')[0]
            posts_data.append(postData)
    

    dates, likes = get_likes()
    _, followers = get_followers()

    # Pass data to the template
    return render(
        request, 'profile.html', {
            "posts": posts_data,
            "user_metrics": user_metrics,
            "likes_today": likes_today,
            "likes_yesterday": likes_yesterday,
            "yesterday_date": yesterday_formatted,
            "week_dates": dates,
            "week_likes": likes,
            "week_followers": followers,
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
            'like_count': likes,
            'comments_count': random.randint(2, 10)
        })


    return posts
