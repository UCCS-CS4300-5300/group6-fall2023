from django.shortcuts import render


# Create your views here.
def profile(request, user_name):
    return render(request, 'profile.html', {"count": [1,2,3]})
