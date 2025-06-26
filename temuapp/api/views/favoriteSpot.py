from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from temuapp.models import FavoriteSpot, TouristSpot
from ..serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_spot(request, spot_id):
    user = request.user
    try:
        spot = TouristSpot.objects.get(pk=spot_id)
    except TouristSpot.DoesNotExist:
        return Response({"message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)
    fav, created = FavoriteSpot.objects.get_or_create(user=user, spot=spot)
    if not created:
        return Response({"message": "Spot already in favorites"}, status=status.HTTP_200_OK)
    return Response({"message": "Spot added to favorites"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite_spot(request, spot_id):
    user = request.user
    try:
        fav = FavoriteSpot.objects.get(user=user, spot_id=spot_id)
        fav.delete()
        return Response({"message": "Spot removed from favorites"}, status=status.HTTP_200_OK)
    except FavoriteSpot.DoesNotExist:
        return Response({"message": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite_spots(request):
    user = request.user
    favorites = FavoriteSpot.objects.filter(user=user).select_related('spot')
    spots = [fav.spot for fav in favorites]
    serializer = TouristSpotSerializer(spots, many=True)
    return Response({"favorites": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def most_favorited_spots(request):
    spots = (
        TouristSpot.objects
        .filter(favorited_by__isnull=False)
        .annotate(favorite_count=Count('favorited_by'))
        .order_by('-favorite_count')
    )
    serializer = TouristSpotSerializer(spots, many=True, context={'request': request})
    data = [
        {**spot, "favorite_count": spots[i].favorite_count}
        for i, spot in enumerate(serializer.data)
    ]
    return Response({"most_favorited": data})