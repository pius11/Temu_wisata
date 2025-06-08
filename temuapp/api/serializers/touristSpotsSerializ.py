from temuapp.models import TouristSpot, User, SpotImage
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'role', 'no_hp', 'foto_profile', 'alamat']

class SpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotImage
        fields = ['image_id', 'file_name', 'is_primary', 'uploaded_at']

class TouristSpotSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    images = SpotImageSerializer(many=True, read_only=True)

    class Meta:
        model = TouristSpot
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user_id'] = UserSerializer(instance.user_id).data
        return rep