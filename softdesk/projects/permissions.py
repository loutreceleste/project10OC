from django.shortcuts import get_object_or_404
from rest_framework import permissions
from projects.models import Project

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only the owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests (SAFE_METHODS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the requesting user is the owner of the object
        return obj.author == request.user

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only the author of a project to edit it.
    """
    message = "Vous n'êtes pas l'auteur de cette ressource."

    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests (SAFE_METHODS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the requesting user is the author of the project
        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        return project.author == request.user

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests (SAFE_METHODS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the requesting user is the author of the project
        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        return project.author == request.user or request.method in permissions.SAFE_METHODS

class IsContributorOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only contributors of a project to edit it.
    """
    message = "Vous n'êtes pas contributeur de ce projet."

    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests (SAFE_METHODS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the requesting user is a contributor of the project
        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        return project.contributor_projects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests (SAFE_METHODS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the requesting user is a contributor of the project
        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        return project.contributor_projects.filter(user=request.user).exists() or request.method in permissions.SAFE_METHODS
