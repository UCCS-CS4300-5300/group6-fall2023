from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def profile(request, user_name):
    return render(request, 'profile.html', {"count": [1,2,3]})

def connectInsta(request):
    print(request.body)
    return JsonResponse({
        "status": "success"
    })
