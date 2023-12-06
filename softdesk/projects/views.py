from projects.serializers import ProjectSerializer, ContributorSerializer
from projects.models import Project, Contributor
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class ProjectViewSet(ModelViewSet):
        serializer_class = ProjectSerializer

        def get_queryset(self):
                return Project.objects.prefetch_related('contributors').all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un projet.")
                serializer.save(author=self.request.user)



class ContributorViewSet(ModelViewSet):
        serializer_class = ContributorSerializer
        def get_queryset(self):
                return Contributor.objects.all()


        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un contributeur.")
                serializer.save(user=self.request.user)
