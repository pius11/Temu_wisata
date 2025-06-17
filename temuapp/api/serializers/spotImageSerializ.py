from rest_framework import serializers
from temuapp.models import SpotImage

class SpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotImage
        fields = ['image_id', 'file_name', 'is_primary', 'uploaded_at']