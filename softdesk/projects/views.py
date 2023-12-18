from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from projects.permissions import IsOwnerOrReadOnly, IsPartOfProject, IsContributorOfIssueProject
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.permissions import IsContributorOfProject
from authentication.models import User


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(author=user) | Q(contributors__user=user)).distinct()

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise ValidationError("Vous devez être authentifié pour créer un projet.")
        serializer.save(author=self.request.user)

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        author = self.request.user
        user_id = self.request.data.get('user')
        project_ids = self.request.data.get('projects', [])

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")

        projects = []
        for project_id in project_ids:
            try:
                project = Project.objects.get(pk=project_id, author=author)
                projects.append(project)
            except Project.DoesNotExist:
                raise ValidationError(f"Project with ID {project_id} does not exist or you're not the author")

        contributor = serializer.save(author=author, user=user)
        contributor.projects.set(projects)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Issues.objects.filter(Q(author=user) | Q(projects__contributors__user=user)).distinct()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project, author=self.request.user)

class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(author=user)

    def perform_create(self, serializer):
        issues_id = self.kwargs.get('issue_pk')
        issue = Issues.objects.get(pk=issues_id)
        serializer.save(issue=issue, author=self.request.user)

class ProjectsIssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsContributorOfProject]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return Issues.objects.filter(projects_id=project_pk)

class ProjectsContributorsViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        return Contributor.objects.filter(projects=project)

class IssuesCommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        project = Project.objects.get(pk=project_pk)
        return Comments.objects.filter(issue_id=issue_pk)
