from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'popularity_assessor'
urlpatterns = [
    # path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='popularity_assessor:login'), name='logout'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('connect-insta/', views.connectInsta, name="connect-insta"),
    path('connect-facebook/', views.connectFacebook, name="connect-facebook"),
    path('facebook-auth/', views.redirectToFacebookAuth, name="facebook-auth"),
    path('timed_metrics/', views.timed_metrics, name='timed-metrics'),
    # path('profile/<str:user_name>/post/<int:post_id>', views.post, name='post')
]
