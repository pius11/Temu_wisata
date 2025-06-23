from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from temuapp.models import Testimoni, TestimoniImage, TouristSpot
from ..serializers.testimoniSerializ import TestimoniSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_testimoni(request, spot_id):
    user = request.user
    testi_text = request.data.get('testi_text', '')
    spot = TouristSpot.objects.filter(pk=spot_id).first()
    if not spot:
        return Response({"message": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)
    testimoni = Testimoni.objects.create(
        spot=spot,
        user=user,
        testi_text=testi_text
    )
    images = request.FILES.getlist('images')
    for img in images:
        TestimoniImage.objects.create(
            testimoni=testimoni,
            file_name=img
        )
    serializer = TestimoniSerializer(testimoni)
    return Response({"message": "Testimoni created", "data": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_testimoni_by_spot(request, spot_id):
    testimonis = Testimoni.objects.filter(spot_id=spot_id).select_related('user').prefetch_related('images')
    serializer = TestimoniSerializer(testimonis, many=True)
    return Response({"testimonies": serializer.data}, status=status.HTTP_200_OK)