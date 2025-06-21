# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from temuapp.models import Review
# from ..serializers.reviewSerializ import ReviewSerializer

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_reviews_by_spot(request, spot_id):
#     reviews = Review.objects.filter(spot_id=spot_id)
#     serializer = ReviewSerializer(reviews, many=True)
#     return Response({"code": 2000, "message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)