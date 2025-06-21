# from rest_framework.decorators import api_view, permission_classes, parser_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# # from temuapp.models import Review, ReviewImage
# from ..serializers.reviewSerializ import ReviewSerializer
# from ..serializers.reviewImageSerializ import ReviewImageSerializer
# from rest_framework.parsers import MultiPartParser, FormParser

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])  # Tambahkan parser untuk handle file upload
# def create_review(request):
#     data = request.data.copy()
#     data['user_id'] = request.user.id

#     # Handle text data untuk review
#     review_serializer = ReviewSerializer(data=data)
#     if review_serializer.is_valid():
#         review = review_serializer.save()
        
#         # Handle multiple image uploads
#         images = request.FILES.getlist('images')  # Ambil semua file dengan key 'images'
#         image_objs = []
#         for img in images:
#             image_obj = ReviewImage.objects.create(
#                 review_id=review,
#                 file_name=img  # Simpan file langsung ke ImageField
#             )
#             image_objs.append(image_obj)
        
#         images_data = ReviewImageSerializer(image_objs, many=True).data
#         response_data = review_serializer.data
#         response_data['images'] = images_data
#         return Response({
#             "code": 2001,
#             "message": "Review & images created successfully",
#             "data": response_data
#         }, status=status.HTTP_201_CREATED)
    
#     return Response({
#         "code": 4001,
#         "message": "Error in review data",
#         "errors": review_serializer.errors
#     }, status=status.HTTP_400_BAD_REQUEST)