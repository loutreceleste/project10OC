from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from projects.permissions import IsOwnerOrReadOnly

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise ValidationError("Vous devez être authentifié pour créer un projet.")
        serializer.save(author=self.request.user)

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Contributor.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project, author=self.request.user)

class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Issues.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project, author=self.request.user)

class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comments.objects.all()

    def perform_create(self, serializer):
        issues_id = self.kwargs.get('issue_pk')
        issue = Issues.objects.get(pk=issues_id)
        serializer.save(issue=issue, author=self.request.user)

class ProjectsIssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return Issues.objects.filter(projects_id=project_pk)

class ProjectsContributorsViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return Issues.objects.filter(projects_id=project_pk)

class IssuesCommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        project = Project.objects.get(pk=project_pk)
        return Comments.objects.filter(issue_id=issue_pk)