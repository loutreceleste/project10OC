from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor
from rest_framework import serializers

from projects.models import Issues


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'projects')

class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)  # Serializer pour la liste des contributeurs

    class Meta:
        model = Project
        fields = '__all__'

class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'