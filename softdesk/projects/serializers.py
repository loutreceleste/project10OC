from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from projects.models import Project, Contributor, Comments, Issues
from authentication.models import User

# Serializer for the Contributor model
class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'author', 'projects')

# Serializer for the Comments model
class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'  # Includes all fields from the Comments model

# Serializer for the Issues model
class IssuesSerializer(serializers.ModelSerializer):
    comments_issues = CommentsSerializer(many=True, read_only=True)  # Nested serializer for related Comments
    contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Issues
        fields = ['id', 'name', 'author', 'nature', 'priority', 'progression', 'description', 'created_time',
                  'contributors', 'comments_issues']

# Serializer for the Project model
class ProjectSerializer(serializers.ModelSerializer):
    contributors_projects = ContributorSerializer(many=True, read_only=True)  # Nested serializer for related Contributors
    issues_projects = IssuesSerializer(many=True, read_only=True)  # Nested serializer for related Issues

    class Meta:
        model = Project
        fields = ('id', 'author', 'name', 'created_time', 'type', 'description', 'contributors_projects', 'issues_projects')
