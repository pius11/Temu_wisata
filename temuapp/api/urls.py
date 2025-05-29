from django.urls import path
from .views import create_user

urlpatterns = [
    path('users/', create_user, name='create-user'),
]
