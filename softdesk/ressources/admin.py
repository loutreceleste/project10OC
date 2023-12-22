from django.contrib import admin
from .models import Project, Contributor, Issues, Comments


class AllProject(admin.ModelAdmin):
    list_display = ('name', 'author', 'type', 'created_time')
    search_fields = ('type',)
    list_filter = ('type',)

admin.site.register(Project, AllProject)

class ProjectContributors(admin.ModelAdmin):
    list_display = ('user', 'projects', 'created_time')
    list_filter = ('projects',)

admin.site.register(Contributor, ProjectContributors)

class ProjectIssues(admin.ModelAdmin):
    list_display = ('name', 'author', 'projects', 'created_time')
    list_filter = ('projects',)

admin.site.register(Issues, ProjectIssues)

class ProjectComments(admin.ModelAdmin):
    list_display = ('id', 'author', 'issue', 'created_time')
    list_filter = ('issue',)

admin.site.register(Comments, ProjectComments)