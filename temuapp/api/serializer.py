from rest_framework import serializers
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