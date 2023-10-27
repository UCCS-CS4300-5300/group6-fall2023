from django.urls import path
from . import views

app_name = 'popularity_assessor'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login, name='login'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('profile/<str:user_name>/post/<int:post_id>', views.post, name='post')
]