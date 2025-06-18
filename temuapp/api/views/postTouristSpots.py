from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import TouristSpot, SpotImage
from ..serializers.touristSpotsSerializ import TouristSpotSerializer
from ..serializers.spotImageSerializ import SpotImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_tourist_spot(request):
    data = request.data.copy()
    data['user_id'] = request.user.id

    spot_serializer = TouristSpotSerializer(data=data)
    if spot_serializer.is_valid():
        spot = spot_serializer.save()
        images = request.FILES.getlist('images')
        image_objs = []
        for idx, img in enumerate(images):
            image_obj = SpotImage.objects.create(
                spot_id=spot,
                file_name=img,  # file_name sekarang adalah ImageField
                is_primary=(idx == 0)  # gambar pertama jadi primary
            )
            image_objs.append(image_obj)
        images_data = SpotImageSerializer(image_objs, many=True).data
        response_data = spot_serializer.data
        response_data['images'] = images_data
        return Response({"code": 2001, "message": "Tourist spot & images created", "data": response_data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": spot_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)