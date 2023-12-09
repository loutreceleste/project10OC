from django.contrib import admin
from .models import Project, Contributor, Issues, Comments


class ProjectsProject(admin.ModelAdmin):
    list_display = ('name', 'author', 'type')
    search_fields = ('type',)
    list_filter = ('type',)

admin.site.register(Project, ProjectsProject)

class ProjectsContributor(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Contributor, ProjectsContributor)

class IssuesContributor(admin.ModelAdmin):
    display = '__all__'

admin.site.register(Issues, IssuesContributor)

class CommentsContributor(admin.ModelAdmin):
    display = '__all__'

admin.site.register(Comments, CommentsContributor)