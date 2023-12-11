from django.shortcuts import render
from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ContributorViewSet(ModelViewSet):
        serializer_class = ContributorSerializer
        def get_queryset(self):
                return Contributor.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un contributeur.")
                serializer.save(author=self.request.user)

        def list(self, request, project_id=None):
                if project_id is not None:
                        contributors = Contributor.objects.filter(projects__id=project_id)
                        users = contributors.values_list('user__username', flat=True)
                        contributors_list = list(users)
                        return Response({"Contributors": contributors_list})
                else:
                        return super().list(request)

        def get_issues(self, request, contributor_id=None):
                if contributor_id:
                        try:
                                contributor = Contributor.objects.get(id=contributor_id)
                                issues = contributor.issues.all()  # Récupérer tous les problèmes liés à ce contributeur
                                serialized_issues = IssuesSerializer(issues, many=True).data
                                return Response({"Issues": serialized_issues})
                        except Contributor.DoesNotExist:
                                return Response({"message": "Aucun contributeur trouvé avec cet ID."},
                                                status=status.HTTP_404_NOT_FOUND)
                else:
                        return Response({"message": "ID du contributeur non fourni."},
                                        status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(ModelViewSet):
        serializer_class = ProjectSerializer

        def get_queryset(self):
                return Project.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un projet.")
                serializer.save(author=self.request.user)

        def list(self, request, project_id=None):
                if project_id is not None:
                        issues = Issues.objects.filter(projects__id=project_id)
                        serialized_issues = self.get_serializer(issues, many=True).data
                        return Response({"Issues": serialized_issues})
                else:
                        return super().list(request)


class IssuesViewSet(ModelViewSet):
        serializer_class = IssuesSerializer
        def get_queryset(self):
                return Issues.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un problème.")
                serializer.save(author=self.request.user)

class CommentsViewSet(ModelViewSet):
        serializer_class = CommentsSerializer
        def get_queryset(self):
                return Comments.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un commentaire.")
                serializer.save(author=self.request.user)

