from rest_framework.serializers import ModelSerializer
from authentication.models import User
from rest_framework import serializers

# Serializer for the User model
class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    can_be_contacted = serializers.CharField(write_only=True)
    can_data_be_shared = serializers.CharField(write_only=True)
    birthday = serializers.CharField(write_only=True)
    created_time = serializers.CharField(write_only=True)
    last_login = serializers.CharField(write_only=True)
    is_active = serializers.CharField(write_only=True)

    class Meta:
        model = User  # Specifies the model this serializer is associated with
        # Specifies the fields from the User model to be included in the serialized representation
        fields = ('id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'birthday', 'created_time',
                  'last_login', 'is_active')
