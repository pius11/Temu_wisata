from rest_framework import serializers
from temuapp.models import Testimoni, TestimoniImage

class TestimoniImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimoniImage
        fields = ['image_id', 'file_name', 'uploaded_at']

class TestimoniSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    foto_profile = serializers.SerializerMethodField()
    images = TestimoniImageSerializer(many=True, read_only=True)

    class Meta:
        model = Testimoni
        fields = ['testimoni_id', 'username', 'foto_profile', 'testi_text', 'images', 'created_at']

    def get_foto_profile(self, obj):
        if obj.user.foto_profile and hasattr(obj.user.foto_profile, 'url'):
            return obj.user.foto_profile.url
        return '/media/profile_images/default_profile.jpg'