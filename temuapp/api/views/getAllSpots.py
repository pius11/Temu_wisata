from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot
from ..serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def list_tourist_spots(request):
    spots = TouristSpot.objects.all()
    serializer = TouristSpotSerializer(spots, many=True)
    return Response({"code": 2000, "message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def count_verified_spots(request):
    total_verified_spots = TouristSpot.objects.filter(is_verified=True).count()
    return Response({"code": 2000, "message": "Success", "total_verified_tourist_spots": total_verified_spots}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tourist_spot_by_id(request, spot_id):
    try:
        spot = TouristSpot.objects.get(pk=spot_id)
    except TouristSpot.DoesNotExist:
        return Response({"code": 404, "message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TouristSpotSerializer(spot)
    return Response({"code": 2000, "message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)