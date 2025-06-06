from rest_framework import serializers
from temuapp.models import TouristSpot, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'role', 'no_hp', 'foto_profile', 'alamat']

class TouristSpotSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = TouristSpot
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Ganti user_id dengan nested user info saat GET
        rep['user_id'] = UserSerializer(instance.user_id).data
        return rep