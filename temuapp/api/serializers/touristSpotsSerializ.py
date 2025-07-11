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
    image = serializers.SerializerMethodField()

    class Meta:
        model = TouristSpot
        fields = '__all__'  # atau sebutkan field satu per satu, pastikan 'image' masuk

    def get_image(self, obj):
        primary_img = obj.images.filter(is_primary=True).first()
        if primary_img and primary_img.file_name:
            request = self.context.get('request')
            url = primary_img.file_name.url
            return request.build_absolute_uri(url) if request else url
        # fallback: gambar pertama jika tidak ada primary
        first_img = obj.images.first()
        if first_img and first_img.file_name:
            request = self.context.get('request')
            url = first_img.file_name.url
            return request.build_absolute_uri(url) if request else url
        return None