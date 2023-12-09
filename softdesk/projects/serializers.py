from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor, Comments
from rest_framework import serializers

from projects.models import Issues

class ProjectChoiceField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return Project.objects.filter(author=request.user)
        return Project.objects.none()

class ContributorSerializer(ModelSerializer):
    projects = ProjectChoiceField(queryset=Project.objects.none(), many=True)

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

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'