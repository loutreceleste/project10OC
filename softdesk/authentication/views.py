from datetime import date

from authentication.models import User
from authentication.serializers import UserSerializer

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class UsersViewset(ModelViewSet):
        serializer_class = UserSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
                user = self.request.user
                return User.objects.filter(id=user.id) if user.is_authenticated else User.objects.none()

        def perform_create(self, serializer):
                validated_data = serializer.validated_data
                birthday = validated_data.get('birthday')

                if birthday is None:
                        raise ValidationError("La date de naissance de l'utilisateur n'est pas définie.")

                today = date.today()
                age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

                if age < 15:
                        raise ValidationError("Vous devez avoir au moins 15 ans pour vous enregistrer.")

                validated_data['is_active'] = True

                serializer.save()
