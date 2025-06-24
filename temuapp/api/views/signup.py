from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from ..serializers.userSeriali import UserSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 2001, "message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"code": 4001, "message": "Error in serializer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)