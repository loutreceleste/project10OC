from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor, Comments, Issues
from rest_framework import serializers


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'projects')

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class IssuesSerializer(serializers.ModelSerializer):
    comment_issue = CommentsSerializer(many=True, read_only=True)
    class Meta:
        model = Issues
        fields = ('id', 'author', 'name', 'projects', 'created_time', 'nature', 'priority', 'progression',
                  'description', 'contributor_issues', 'comment_issue')

class ProjectSerializer(serializers.ModelSerializer):
    contributor_projects = ContributorSerializer(many=True, read_only=True)
    issue_project = IssuesSerializer (many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'author', 'name', 'created_time', 'type', 'description', 'contributor_projects', 'issue_project')

