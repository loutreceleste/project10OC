from rest_framework.serializers import ModelSerializer
from authentication.models import User

class UserSerializer(ModelSerializer):
    class Meta:
         model = User
         fields = ('id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'birthday', 'created_time',
                   'last_login')