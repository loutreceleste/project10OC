from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor, Comments, Issues
from rest_framework import serializers


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
    class Meta:
        model = Issues
        fields = ('id', 'author', 'name', 'projects', 'created_time', 'nature', 'priority', 'progression',
                  'description', 'comments_issues')

class ProjectSerializer(serializers.ModelSerializer):
    contributors_projects = ContributorSerializer(many=True, read_only=True)
    issues_projects = IssuesSerializer (many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'author', 'name', 'created_time', 'type', 'description', 'contributors_projects', 'issues_projects')

