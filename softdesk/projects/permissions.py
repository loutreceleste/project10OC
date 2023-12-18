from rest_framework import permissions

from projects.models import Project

from projects.models import Contributor

from projects.models import Issues


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributorOfProject(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            contributor = Contributor.objects.filter(user=request.user).first()
        except Contributor.DoesNotExist:
            return False

        if contributor:
            project_id = view.kwargs.get('project_id')
            is_contributor = Project.objects.filter(pk=project_id, contributors=contributor).exists()
            return is_contributor

        return False


class IsContributorOfIssueProject(permissions.BasePermission):
    def has_permission(self, request, view):
        issue_id = view.kwargs.get('issue_pk')
        try:
            issue = Issues.objects.get(pk=issue_id)
        except Issues.DoesNotExist:
            return False

        return issue.projects.contributors.filter(user=request.user).exists()

class IsPartOfProject(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        issue_id = view.kwargs.get('issue_pk')
        try:
            issue = Issues.objects.get(pk=issue_id)
        except Issues.DoesNotExist:
            return False

        project = issue.projects

        return project.contributors.filter(user=request.user).exists()
