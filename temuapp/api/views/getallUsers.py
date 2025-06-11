from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from temuapp.models import User
from ..serializers.userSeriali import UserSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"code": 2000, "message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)