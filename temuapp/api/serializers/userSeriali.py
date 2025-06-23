from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from temuapp.models import User
import os
from django.conf import settings
from django.core.files import File


class UserSerializer(serializers.ModelSerializer):
    foto_profile = serializers.ImageField(required=False, allow_null=True)

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
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.foto_profile and hasattr(instance.foto_profile, 'url'):
            rep['foto_profile'] = instance.foto_profile.url
        else:
            rep['foto_profile'] = '/media/profile_images/default_profile.jpg'
        return rep

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        if not validated_data.get('foto_profile'):
            validated_data['foto_profile'] = 'profile_images/default_profile.jpg'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)

