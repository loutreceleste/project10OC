from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor
from rest_framework import serializers

from authentication.models import User


class ContributorSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())  # Champ pour sélectionner un utilisateur existant
    projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())  # Champ pour sélectionner un projet existant
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'projects')

class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)  # Serializer pour la liste des contributeurs

    class Meta:
        model = Project
        fields = ('id', 'type', 'author', 'name', 'description', 'created_time', 'contributors')



