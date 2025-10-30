from rest_framework import serializers
from .models import User, DeviceSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "avatar"]


class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = ["id", "device_name", "created_at", "last_seen", "revoked"]
