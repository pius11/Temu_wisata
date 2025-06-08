from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot, SpotImage
from ..serializers.touristSpotsSerializ import TouristSpotSerializer
from ..serializers.spotImageSerializ import SpotImageSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tourist_spot(request):
    data = request.data.copy()
    data['user_id'] = request.user.id

    # Ambil daftar nama file gambar dari frontend (bisa dari JSON atau form-data)
    images = request.data.get('images', [])
    if isinstance(images, str):
        # Jika dikirim sebagai string (misal dari form-data), coba parse ke list
        import json
        try:
            images = json.loads(images)
        except Exception:
            images = [images]  # fallback: single string jadi list

    spot_serializer = TouristSpotSerializer(data=data)
    if spot_serializer.is_valid():
        spot = spot_serializer.save()
        image_objs = []
        for file_name in images:
            image_obj = SpotImage.objects.create(
                spot_id=spot,
                file_name=file_name,
                is_primary=False
            )
            image_objs.append(image_obj)
        images_data = SpotImageSerializer(image_objs, many=True).data
        response_data = spot_serializer.data
        response_data['images'] = images_data
        return Response({"code": 2001, "message": "Tourist spot & images created", "data": response_data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": spot_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)