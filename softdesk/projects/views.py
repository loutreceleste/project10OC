from django.shortcuts import render
from projects.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer
from projects.models import Project, Contributor, Issues, Comments
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
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

class ProjectViewSet(ModelViewSet):
        serializer_class = ProjectSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
                return Project.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un projet.")
                serializer.save(author=self.request.user)

        def get_issues(self, request, project_id=None):
                if project_id:
                        try:
                                project = Contributor.objects.get(id=project_id)
                                issues = project.issues.all()
                                serialized_issues = IssuesSerializer(issues, many=True).data
                                return Response({"Issues": serialized_issues})
                        except Project.DoesNotExist:
                                return Response({"message": "Aucune issue trouvé avec cet ID."},
                                                status=status.HTTP_404_NOT_FOUND)
                else:
                        return Response({"message": "ID du projet non fourni."},
                                        status=status.HTTP_400_BAD_REQUEST)

        def get_contributors(self, request, project_id=None):
                if project_id is not None:
                        contributors = Contributor.objects.filter(projects__id=project_id)
                        users = contributors.values_list('user__username', flat=True)
                        contributors_list = list(users)
                        return Response({"Contributors": contributors_list})
                else:
                        return super().list(request)


class IssuesViewSet(ModelViewSet):
        serializer_class = IssuesSerializer
        def get_queryset(self, project_id=None):
                return Issues.objects.filter(projects__id=project_id)

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un problème.")
                serializer.save(author=self.request.user)

        def get_comments(self, request, issues_id=None):
                if issues_id:
                        try:
                                comments = Comments.objects.filter(issue_id=issues_id)
                                serialized_comments = CommentsSerializer(comments, many=True).data
                                return Response({"Comments": serialized_comments})
                        except Issues.DoesNotExist:
                                return Response({"message": "Aucun problème trouvé avec cet ID."},
                                                status=status.HTTP_404_NOT_FOUND)
                else:
                        return Response({"message": "ID du problème non fourni."}, status=status.HTTP_400_BAD_REQUEST)

class CommentsViewSet(ModelViewSet):

        serializer_class = CommentsSerializer

        def get_queryset(self):
                return Comments.objects.all()

        def perform_create(self, serializer):
                if self.request.user.is_anonymous:
                        raise ValidationError("Vous devez être authentifié pour créer un commentaire.")
                serializer.save(author=self.request.user)
