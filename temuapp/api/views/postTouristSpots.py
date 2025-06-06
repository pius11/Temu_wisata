from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot
from ..serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tourist_spot(request):
    print("User:", request.user)
    print("Is authenticated:", request.user.is_authenticated)
    
    data = request.data.copy()
    data['user_id'] = request.user.id  # Ambil user dari token JWT
    serializer = TouristSpotSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 2001, "message": "Tourist spot created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)