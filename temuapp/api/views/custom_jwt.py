from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from temuapp.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
        if not check_password(password, user.password):
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'alamat': user.alamat,
            'foto_profile': user.foto_profile.url if user.foto_profile and hasattr(user.foto_profile, 'url') else '/media/profile_images/default_profile.jpg',
            'role': user.role,
            'no_hp': user.no_hp,
        }
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer