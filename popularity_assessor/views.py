from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .helpers import get_password_validators_help_texts
from datetime import datetime, timedelta # for mock data
import random


def connectInsta(request):
    return JsonResponse({"status": "success"})


def delete_account(user=None):
    if user is not None:
        user.delete()
    else:
        raise User.DoesNotExist


@login_required
def profile(request, user_name):
    if request.method == "POST":
        user_to_delete = request.user
        delete_account(user_to_delete)
        return redirect('popularity_assessor:login')

    # Call the get_posts method to get the posts data
    posts = get_posts()

    # Aggregate likes for yesterday
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    total_likes_yesterday = sum(sum(1 for like in post['likes'] if like['date'] == yesterday) for post in posts)

    # Call the get_user_metrics method to get the user metrics
    user_metrics = get_user_metrics()

    # Pass both posts data, user metrics, and likes metrics to the template
    return render(request, 'profile.html', {
        "count": [1, 2, 3],
        "posts": posts, 
        "user_metrics": user_metrics,
        "total_likes_today": sum(post['likes_today'] for post in posts),
        "total_likes_yesterday": total_likes_yesterday,
        "yesterday": yesterday
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


def get_mock_likes(num_likes, days_ago=0):
    """ Generate mock likes for a given number of days ago """
    date = datetime.now() - timedelta(days=days_ago)
    return [{'date': date.strftime("%Y-%m-%d")} for _ in range(num_likes)]

def generate_random_likes():
    """ Generate a random number of likes for different days """
    likes = []
    # Random likes from today
    likes.extend(get_mock_likes(random.randint(10, 50), days_ago=0))
    # Random likes from the past few days
    for days_ago in range(1, 5):
        likes.extend(get_mock_likes(random.randint(5, 20), days_ago=days_ago))
    return likes

def get_posts():
    today = datetime.now().strftime("%Y-%m-%d")

    # Mock posts data
    posts = [
        {
            'image_path': f'path/to/image{i}.jpg',
            'title': f'Post {i}',
            'date': '2021-01-0' + str(i),
            'likes': generate_random_likes(),
            'num_comments': random.randint(2, 10)
        } for i in range(1, 6)  # Generating 5 mock posts
    ]

    # Calculate likes for today for each post
    for post in posts:
        post['likes_today'] = sum(1 for like in post['likes'] if like['date'] == today)

    return posts


def get_mock_followers(num_followers, days_ago=0):
    """ Generate mock followers for a given number of days ago """
    date = datetime.now() - timedelta(days=days_ago)
    return [{'date': date.strftime("%Y-%m-%d")} for _ in range(num_followers)]

def get_user_metrics():
 today = datetime.now().strftime("%Y-%m-%d")
 one_day_ago = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

 # Mock followers data
 followers_data = get_mock_followers(300, 0) + get_mock_followers(50, 1)  # 300 followers from today, 50 from 1 day ago

# Calculate followers for today
 followers_today = sum(1 for follower in followers_data if follower['date'] == today)

 # Calculate followers from 1 day ago
 followers_one_day_ago = sum(1 for follower in followers_data if follower['date'] == one_day_ago)

 # Mock total followers, following, and posts
 total_followers = len(followers_data)
 total_following = 200  # Example number
 total_posts = 100      # Example number

 return {
    'username': 'John Doe',  # Mock username
    'total_followers': total_followers,
    'total_following': total_following,
    'total_posts': total_posts,
    'followers_today': followers_today,
    'followers_one_day_ago': followers_one_day_ago,
 }

