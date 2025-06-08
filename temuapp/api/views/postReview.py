from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import Review, ReviewImage
from ..serializers.reviewSerializ import ReviewSerializer
from ..serializers.reviewImageSerializ import ReviewImageSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    data = request.data.copy()
    data['user_id'] = request.user.id

    # Ambil daftar nama file gambar dari frontend (bisa dari JSON atau form-data)
    images = request.data.get('images', [])
    if isinstance(images, str):
        import json
        try:
            images = json.loads(images)
        except Exception:
            images = [images]

    review_serializer = ReviewSerializer(data=data)
    if review_serializer.is_valid():
        review = review_serializer.save()
        image_objs = []
        for file_name in images:
            image_obj = ReviewImage.objects.create(
                review_id=review,
                file_name=file_name
            )
            image_objs.append(image_obj)
        images_data = ReviewImageSerializer(image_objs, many=True).data
        response_data = review_serializer.data
        response_data['images'] = images_data
        return Response({"code": 2001, "message": "Review & images created", "data": response_data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": review_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)