from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.userSeriali import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser

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