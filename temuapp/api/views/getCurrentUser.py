from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import User
from ..serializers.userSeriali import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({"code": 2000, "message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)