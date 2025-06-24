from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from temuapp.models import TouristSpot, SpotImage
from ..serializers.touristSpotsSerializ import TouristSpotSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_tourist_spot(request, pk):
    try:
        spot = TouristSpot.objects.get(pk=pk)
    except TouristSpot.DoesNotExist:
        return Response({"message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TouristSpotSerializer(spot, data=request.data, partial=True)
    if serializer.is_valid():
        spot = serializer.save()

        # Ambil daftar id gambar yang ingin dihapus
        deleted_images = []
        if 'deleted_images' in request.data:
            deleted_images = request.data.getlist('deleted_images')
        elif 'deleted_images[]' in request.data:
            deleted_images = request.data.getlist('deleted_images[]')

        # Hapus gambar yang dipilih user
        if deleted_images:
            SpotImage.objects.filter(spot_id=spot, image_id__in=deleted_images).delete()

        # Tambahkan gambar baru jika ada
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            for img in images:
                SpotImage.objects.create(
                    spot_id=spot,
                    file_name=img,
                    is_primary=False
                )

        # Pastikan selalu ada satu gambar utama
        remaining_images = SpotImage.objects.filter(spot_id=spot)
        if not remaining_images.filter(is_primary=True).exists() and remaining_images.exists():
            first_img = remaining_images.first()
            first_img.is_primary = True
            first_img.save()

        return Response({"message": "Spot updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)