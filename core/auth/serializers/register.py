from rest_framework import serializers

from core.user.serializers import UserSerializer
from core.user.models import User


class RegisterSerializer(UserSerializer):
    # make sure password is more than 8 char
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'bio', 'email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    