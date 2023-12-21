from django.db.models import Q
from django.shortcuts import get_object_or_404

from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from projects.permissions import IsOwnerOrReadOnly
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User

from projects.permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(author=user) | Q(contributor_projects__user=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProjectsContributorsViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthorOrReadOnly, IsContributorOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        user = self.request.user
        return Contributor.objects.filter(projects=project, projects__contributor_projects__user=user).distinct()

    def perform_create(self, serializer):
        author = self.request.user
        user_id = self.request.data.get('user')
        project_pk = self.kwargs.get('project_pk')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")

        project = get_object_or_404(Project, pk=project_pk)  # Récupère le projet depuis l'URL

        serializer.save(author=author, user=user, projects=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectsIssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthorOrReadOnly, IsContributorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)

        return Issues.objects.filter(projects=project, projects__contributor_projects__user=user).distinct()

    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')

        try:
            project = Project.objects.get(pk=project_pk)
        except User.DoesNotExist:
            raise ValidationError(f"Project with ID {project_pk} does not exist")

        serializer.save(projects=project, author=self.request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class IssuesCommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrReadOnly, IsContributorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        # Vérifie si l'utilisateur est contributeur du projet spécifique
        project = get_object_or_404(Project, pk=project_pk, contributor_projects__user=self.request.user)

        # Récupère l'issue spécifique du projet
        issue = get_object_or_404(Issues, pk=issue_pk, projects=project)

        # Retourne les commentaires spécifiques à l'issue du projet
        return Comments.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issues_id = self.kwargs.get('issue_pk')
        issue = Issues.objects.get(pk=issues_id)
        serializer.save(issue=issue, author=self.request.user)
