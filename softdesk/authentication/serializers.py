from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from authentication.models import User

class UserSerializer(ModelSerializer):
    age = serializers.SerializerMethodField()

    @staticmethod
    def get_age(obj):
        return obj.age()

    class Meta:
         model = User
         fields = ('id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'birthday', 'created_time',
                   'last_login', 'is_staff', 'is_superuser', 'projects', 'age')