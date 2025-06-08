from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from temuapp.models import User


class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        # Hash password sebelum save
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)

