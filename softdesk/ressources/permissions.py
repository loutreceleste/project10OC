from django.shortcuts import get_object_or_404
from rest_framework import permissions

from ressources.models import Project


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Vous n'êtes pas l'auteur de cette ressource."

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        return project.author == request.user

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        return project.author == request.user or request.method in permissions.SAFE_METHODS


class IsContributorOrReadOnly(permissions.BasePermission):
    message = "Vous n'êtes pas contributeur de ce projet."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        return project.contributor_projects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        return project.contributor_projects.filter(user=request.user).exists() or request.method in permissions.SAFE_METHODS

