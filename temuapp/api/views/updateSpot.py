from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from temuapp.models import TouristSpot, SpotImage
from ..serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])  # Ubah di sini
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_tourist_spot(request, pk):
    try:
        spot = TouristSpot.objects.get(pk=pk)
    except TouristSpot.DoesNotExist:
        return Response({"message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TouristSpotSerializer(spot, data=request.data, partial=True)
    if serializer.is_valid():
        spot = serializer.save()
        # Jika ada gambar baru, hapus gambar lama lalu tambah baru
        if 'images' in request.FILES:
            SpotImage.objects.filter(spot_id=spot).delete()
            images = request.FILES.getlist('images')
            for idx, img in enumerate(images):
                SpotImage.objects.create(
                    spot_id=spot,
                    file_name=img,
                    is_primary=(idx == 0)
                )
        return Response({"message": "Spot updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

