from django.urls import path
from .views.signup import create_user
from .views.getallUsers import list_users
from .views.custom_jwt import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.postTouristSpots import create_tourist_spot
from .views.getAllSpots import list_tourist_spots
from .views.updateUser import update_user



urlpatterns = [
    path('users/', create_user, name='create-user'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/all/', list_users, name='list-users'),
    path('touristspots/', create_tourist_spot, name='create-tourist-spot'),
    path('touristspots/all/', list_tourist_spots, name='list-tourist-spots'),
    path('users/<int:user_id>/update/', update_user, name='update-user'),
]