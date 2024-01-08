from datetime import date, datetime
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.permissions import IsSelfOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.hashers import make_password

# ViewSet for handling User model operations
class UsersViewset(ModelViewSet):
    serializer_class = UserSerializer  # Specifies the serializer class to be used
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]  # Specifies permission classes for the viewset

    # Custom method to get the queryset based on the request user
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)  # Retrieves the User object based on the request user's ID
        else:
            return User.objects.none()  # Returns an empty queryset if the user is not authenticated

    # Custom method to perform actions when creating a User instance
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        birthday = validated_data.get('birthday')

        # Validating if birthday field is provided
        if birthday is None:
            raise ValidationError("User's birthday is not defined.")

        # Convertir la chaîne 'birthday' en objet 'date'
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()

        today = date.today()
        # Calculating age based on the provided birthday
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

        # Checking if the user is at least 15 years old before registration
        if age < 15:
            raise ValidationError("You must be at least 15 years old to register.")

        validated_data['is_active'] = True  # Setting is_active to True for the new user

        # Checking if password is provided in request data
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            validated_data['password'] = password  # Assigning hashed password to validated_data

        serializer.save()  # Saving the new user instance
