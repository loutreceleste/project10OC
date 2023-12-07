from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer
from projects.models import Project, Contributor, Issues

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

        def list(self, request, *args, **kwargs):
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                serialized_data = serializer.data

                for project_data in serialized_data:
                        project_id = project_data['id']
                        project = Project.objects.get(id=project_id)
                        contributors = project.contributors.all()
                        contributors_data = [{'id': contributor.id, 'user': contributor.user.id,
                                              'username': contributor.user.username} for contributor in contributors]
                        project_data['contributors'] = contributors_data

                return Response(serialized_data)



class ContributorViewSet(ModelViewSet):
        serializer_class = ContributorSerializer
        def get_queryset(self):
                return Contributor.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un contributeur.")
                serializer.save()

        def list(self, request, project_id=None):
                if project_id is not None:
                        contributors = Contributor.objects.filter(projects__id=project_id)
                        users = contributors.values_list('user__username', flat=True)
                        contributors_list = list(users)
                        return Response({"Contributors": contributors_list})
                else:
                        return super().list(request)

class IssuesViewSet(ModelViewSet):
        serializer_class = IssuesSerializer
        def get_queryset(self):
                return Issues.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un contributeur.")
                serializer.save()
