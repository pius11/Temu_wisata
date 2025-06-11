from rest_framework import serializers
from temuapp.models import Review, ReviewImage, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email']

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image_id', 'file_name', 'uploaded_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # atau ['review_id', 'spot_id', 'user_id', ...]