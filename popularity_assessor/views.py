from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def profile(request, user_name):
    return render(request, 'profile.html', {"count": [1,2,3]})

def register(request):
  # Handle the POST request (form submission)
  if request.method == "POST":
      form = UserCreationForm(request.POST)
      if form.is_valid():
          form.save()
          # Optionally, you can log the user in after registration here
          return redirect('popularity_assessor:login')  # Redirect to login page or some other page
  # Handle the GET request (displaying the form)
  else:
      form = UserCreationForm()

  context = {'form': form}
  return render(request, 'register.html', context)