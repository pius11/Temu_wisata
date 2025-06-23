from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot, SpotImage

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_tourist_spot(request, pk):
    try:
        spot = TouristSpot.objects.get(pk=pk)
    except TouristSpot.DoesNotExist:
        return Response({"message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)
    SpotImage.objects.filter(spot_id=spot).delete()
    spot.delete()
    return Response({"message": "Spot and all images deleted"}, status=status.HTTP_200_OK)