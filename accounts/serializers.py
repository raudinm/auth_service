from rest_framework import serializers
from .models import User, DeviceSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "avatar"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Used for creating a new user.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = ["id", "device_name", "created_at", "last_seen", "revoked"]
