from django.db.models import Q
from django.shortcuts import get_object_or_404
from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from projects.permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly, IsOwnerOrReadOnly
from authentication.models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# ViewSet for managing projects
class ProjectViewSet(ModelViewSet):
    # Set serializer and permission classes
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Retrieve queryset of projects based on user's role (owner or contributor)
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(author=user) | Q(contributor_projects__user=user)).distinct()

    # Perform creation of a new project
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ViewSet for managing contributors related to projects
class ProjectsContributorsViewSet(ModelViewSet):
    # Set serializer and permission classes
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    # Retrieve queryset of contributors for a specific project
    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        user = self.request.user
        return Contributor.objects.filter(projects=project).filter(Q(projects__contributor_projects__user=user) | Q(author=user)).distinct()

    # Perform creation of a new contributor for a project
    def perform_create(self, serializer):
        author = self.request.user
        user_id = self.request.data.get('user')
        project_pk = self.kwargs.get('project_pk')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")

        project = get_object_or_404(Project, pk=project_pk)
        serializer.save(author=author, user=user, projects=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ViewSet for managing issues related to projects
class ProjectsIssuesViewSet(ModelViewSet):
    # Set serializer and permission classes
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    # Retrieve queryset of issues for a specific project
    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        return Issues.objects.filter(projects=project).filter(Q(projects__contributor_projects__user=user) | Q(author=user)).distinct()

    # Custom creation logic for handling issue creation and validation of contributors
    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        contributors = project.contributor_projects.values_list('user_id', flat=True)

        contributor_ids = request.data.get('contributors', [])
        invalid_contributors = [contributor_id for contributor_id in contributor_ids if contributor_id not in contributors]

        if invalid_contributors:
            return Response(f"Ces contributeurs ne font pas partie du projet spécifié: {invalid_contributors}", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, project)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Perform creation of a new issue for a project
    def perform_create(self, serializer, project):
        serializer.save(projects=project, author=self.request.user)

# ViewSet for managing comments related to issues
class IssuesCommentsViewSet(ModelViewSet):
    # Set serializer and permission classes
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    # Retrieve queryset of comments for a specific issue within a project
    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        project = get_object_or_404(Project, pk=project_pk, contributor_projects__user=self.request.user)
        issue = get_object_or_404(Issues, pk=issue_pk, projects=project)

        return Comments.objects.filter(issue=issue)

    # Perform creation of a new comment for an issue
    def perform_create(self, serializer):
        issues_id = self.kwargs.get('issue_pk')
        issue = Issues.objects.get(pk=issues_id)
        serializer.save(issue=issue, author=self.request.user)
