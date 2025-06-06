from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from temuapp.models import User
from ..serializers.userSeriali import UserSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"code": 4002, "message": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            serializer = UserSerializer(user)
            return Response({"code": 2002, "message": "Login successful", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"code": 4003, "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"code": 4004, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)