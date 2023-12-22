from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ressources.models import Project, Contributor, Comments, Issues
from authentication.models import User


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'author', 'projects')

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class IssuesSerializer(serializers.ModelSerializer):
    comments_issues = CommentsSerializer(many=True, read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Issues
        fields = ['id', 'name', 'author', 'nature', 'priority', 'progression', 'description', 'created_time',
                  'contributors', 'comments_issues']

class ProjectSerializer(serializers.ModelSerializer):
    contributors_projects = ContributorSerializer(many=True, read_only=True)
    issues_projects = IssuesSerializer (many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'author', 'name', 'created_time', 'type', 'description', 'contributors_projects', 'issues_projects')

