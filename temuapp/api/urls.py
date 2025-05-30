from django.urls import path
from .views.signup import create_user
from .views.signin import login_user
from .views.custom_jwt import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('users/', create_user, name='create-user'),
    path('users/login/', login_user, name='login-user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]