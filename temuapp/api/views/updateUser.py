from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers.userSeriali import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from temuapp.models import User

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_current_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 2000, "message": "User updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"code": 4001, "message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])  # Ganti ke IsAuthenticated jika hanya user login yang boleh update
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_user_by_pk(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"code": 4040, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 2000, "message": "User updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"code": 4001, "message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)