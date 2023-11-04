from django.shortcuts import render


# Create your views here.
def profile(request, user_name):
  # For now, the only POST request is used to delete account.
  # In the future, this must be checked further to very what the user want. (ex: delete vs. manage metric)
  if request.method == "POST":
    delete_account()
    return render(request, "profile.html", {"count": [1,2,3], "confirm_delete_request": "Account deletion request received."})

  return render(request, 'profile.html', {"count": [1,2,3]})

def delete_account(user_id=None):
  pass
  
