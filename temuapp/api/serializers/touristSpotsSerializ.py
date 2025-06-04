from rest_framework import serializers
from temuapp.models import TouristSpot, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'role', 'no_hp', 'foto_profile', 'alamat']

class TouristSpotSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)  # Nested user data

    class Meta:
        model = TouristSpot
        fields = '__all__'