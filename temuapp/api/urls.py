from django.urls import path
from .views.signup import create_user
from .views.getallUsers import list_users, count_users
from .views.custom_jwt import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.postTouristSpots import create_tourist_spot
from .views.getAllSpots import list_tourist_spots, count_verified_spots, get_tourist_spot_by_id
from .views.updateUser import update_current_user, update_user_by_pk
# from .views.postReview import create_review
# from .views.getAllReviews import list_reviews
# from .views.getReviewsBySpot import get_reviews_by_spot
from .views.getCurrentUser import get_current_user
from .views.ai import chat_ai
from .views.updateSpot import update_tourist_spot
from .views.deleteSpot import delete_tourist_spot
from .views.favoriteSpot import add_favorite_spot, remove_favorite_spot, list_favorite_spots, most_favorited_spots
# from .views.ai import get_chat_history
from django.conf import settings
from django.conf.urls.static import static
from .views.testimoni import create_testimoni, list_testimoni_by_spot



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
    path('users/<int:pk>/update/', update_user_by_pk, name='update-user'),
    # path('reviews/', create_review, name='create-review'),
    # path('reviews/all/', list_reviews, name='list-reviews'),
    # path('reviews/spot/<int:spot_id>/', get_reviews_by_spot, name='get-reviews-by-spot'),
    path('users/me/', get_current_user, name='get-current-user'),
    path('chat/', chat_ai, name='chat-ai'),
    path('touristspots/<int:pk>/update/', update_tourist_spot, name='update-tourist-spot'),
    path('touristspots/<int:pk>/delete/', delete_tourist_spot, name='delete-tourist-spot'),
    path('favorites/', list_favorite_spots, name='list-favorite-spots'),
    path('favorites/add/<int:spot_id>/', add_favorite_spot, name='add-favorite-spot'),
    path('favorites/remove/<int:spot_id>/', remove_favorite_spot, name='remove-favorite-spot'),
    # path('chat/history/<int:session_id>/', get_chat_history, name='get-chat-history'),
    path('testimoni/<int:spot_id>/add/', create_testimoni, name='create-testimoni'),
    path('testimoni/spot/<int:spot_id>/', list_testimoni_by_spot, name='list-testimoni-by-spot'),
    path('touristspots/<int:spot_id>/', get_tourist_spot_by_id, name='get-tourist-spot-by-id'),
    path('most-favorited-spots/', most_favorited_spots),
]