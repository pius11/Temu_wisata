from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from temuapp.models import TouristSpot
from temuapp.api.serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['GET'])
def search_tourist_spot(request):
    query = request.GET.get('q', '')
    if query:
        spots = TouristSpot.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(kota__icontains=query) |
            Q(kecamatan__icontains=query) |
            Q(desa__icontains=query),
            is_removed=False
        )
    else:
        spots = TouristSpot.objects.none()
    serializer = TouristSpotSerializer(spots, many=True)
    return Response(serializer.data)