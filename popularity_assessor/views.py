from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .helpers import get_password_validators_help_texts

  # Create your views here.
@login_required
def profile(request, user_name):
  return render(request, 'profile.html', {"count": [1,2,3]})

def register(request):
  if request.method == "POST":
      form = UserCreationForm(request.POST)
      if form.is_valid():
          form.save()
          # Log the user in after registration and redirect to profile
          new_user = authenticate(username=form.cleaned_data['username'],
                                  password=form.cleaned_data['password1'])
          login(request, new_user)
          return redirect('popularity_assessor:profile', user_name=new_user.username)
  else:
      form = UserCreationForm()

  # Include password help texts in context
  password_help_texts = get_password_validators_help_texts()
  context = {
      'form': form,
      'password_help_texts': password_help_texts
  }
  return render(request, 'register.html', context)

def custom_login(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('popularity_assessor:profile', user_name=user.username)
  else:
    form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})
