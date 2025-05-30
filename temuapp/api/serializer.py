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
            'password_hash',
            'no_hp',
            'foto_profile',
            'alamat',
            'role',
            'created_at'
        ]

    def create(self, validated_data):
        # Hash password sebelum save
        if 'password_hash' in validated_data:
            validated_data['password_hash'] = make_password(validated_data['password_hash'])
        return super().create(validated_data)

