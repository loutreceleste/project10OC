from rest_framework.serializers import ModelSerializer
from authentication.models import User

# Serializer for the User model
class UserSerializer(ModelSerializer):
    class Meta:
        model = User  # Specifies the model this serializer is associated with
        # Specifies the fields from the User model to be included in the serialized representation
        fields = ('id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'birthday', 'created_time',
                  'last_login', 'is_active')
