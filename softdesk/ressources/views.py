from django.db.models import Q
from django.shortcuts import get_object_or_404

from ressources.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from ressources.models import Project, Contributor, Issues, Comments
from ressources.permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly, IsOwnerOrReadOnly
from authentication.models import User


from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(author=user) | Q(contributor_projects__user=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProjectsContributorsViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        user = self.request.user
        return Contributor.objects.filter( projects=project).filter( Q(projects__contributor_projects__user=user) |
                                                                     Q(author=user)).distinct()

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
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)

        return Issues.objects.filter( projects=project).filter( Q(projects__contributor_projects__user=user) |
                                                                     Q(author=user)).distinct()

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

    def perform_create(self, serializer, project):
        serializer.save(projects=project, author=self.request.user)

class IssuesCommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly | IsContributorOrReadOnly]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        project = get_object_or_404(Project, pk=project_pk, contributor_projects__user=self.request.user)
        issue = get_object_or_404(Issues, pk=issue_pk, projects=project)

        return Comments.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issues_id = self.kwargs.get('issue_pk')
        issue = Issues.objects.get(pk=issues_id)
        serializer.save(issue=issue, author=self.request.user)
