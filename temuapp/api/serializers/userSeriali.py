from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from temuapp.models import User
import os
from django.conf import settings
from django.core.files import File


class UserSerializer(serializers.ModelSerializer):
    foto_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'password',
            'no_hp',
            'foto_profile',
            'alamat',
            'role',
            'created_at'
        ]

    def get_foto_profile(self, obj):
        if obj.foto_profile and hasattr(obj.foto_profile, 'url'):
            return obj.foto_profile.url
        return '/media/profile_images/default_profile.jpg'

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # Set path default jika tidak upload foto
        if not validated_data.get('foto_profile'):
            validated_data['foto_profile'] = 'profile_images/default_profile.jpg'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)

