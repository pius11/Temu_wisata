from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import User
from ..serializers.userSeriali import UserSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"code": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 200, "message": "User updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"code": 400, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)