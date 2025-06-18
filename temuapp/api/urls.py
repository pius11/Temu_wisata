from django.urls import path
from .views.signup import create_user
from .views.getallUsers import list_users, count_users
from .views.custom_jwt import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.postTouristSpots import create_tourist_spot
from .views.getAllSpots import list_tourist_spots, count_verified_spots
from .views.updateUser import update_current_user
from .views.postReview import create_review
from .views.getAllReviews import list_reviews
from .views.getReviewsBySpot import get_reviews_by_spot
from .views.getCurrentUser import get_current_user
from .views.ai import chat_ai
from .views.updateSpot import update_tourist_spot
from .views.deleteSpot import delete_tourist_spot
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('users/', create_user, name='create-user'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/all/', list_users, name='list-users'),
    path('users/count/', count_users, name='count-users'),
    path('touristspots/', create_tourist_spot, name='create-tourist-spot'),
    path('touristspots/all/', list_tourist_spots, name='list-tourist-spots'),
    path('touristspots/count-verified/', count_verified_spots, name='count-verified-spots'),
    path('users/me/update/', update_current_user, name='update-user'),
    path('reviews/', create_review, name='create-review'),
    path('reviews/all/', list_reviews, name='list-reviews'),
    path('reviews/spot/<int:spot_id>/', get_reviews_by_spot, name='get-reviews-by-spot'),
    path('users/me/', get_current_user, name='get-current-user'),
    path('chat/', chat_ai, name='chat-ai'),
    path('touristspots/<int:pk>/update/', update_tourist_spot, name='update-tourist-spot'),
    path('touristspots/<int:pk>/delete/', delete_tourist_spot, name='delete-tourist-spot'),
]