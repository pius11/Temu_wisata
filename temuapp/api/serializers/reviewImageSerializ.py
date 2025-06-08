from rest_framework import serializers
from temuapp.models import ReviewImage

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image_id', 'file_name', 'uploaded_at']