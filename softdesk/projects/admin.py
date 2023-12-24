from django.contrib import admin
from projects.models import Project, Contributor, Issues, Comments

# Custom admin configuration for Project model
class AllProject(admin.ModelAdmin):
    list_display = ('name', 'author', 'type', 'created_time')  # Fields to display in the admin list view
    search_fields = ('type',)  # Fields available for search
    list_filter = ('type',)  # Fields available for filtering

# Registering the Project model with custom admin configuration
admin.site.register(Project, AllProject)

# Custom admin configuration for Contributor model
class ProjectContributors(admin.ModelAdmin):
    list_display = ('user', 'projects', 'created_time')  # Fields to display in the admin list view
    list_filter = ('projects',)  # Fields available for filtering

# Registering the Contributor model with custom admin configuration
admin.site.register(Contributor, ProjectContributors)

# Custom admin configuration for Issues model
class ProjectIssues(admin.ModelAdmin):
    list_display = ('name', 'author', 'projects', 'created_time')  # Fields to display in the admin list view
    list_filter = ('projects',)  # Fields available for filtering

# Registering the Issues model with custom admin configuration
admin.site.register(Issues, ProjectIssues)

# Custom admin configuration for Comments model
class ProjectComments(admin.ModelAdmin):
    list_display = ('id', 'author', 'issue', 'created_time')  # Fields to display in the admin list view
    list_filter = ('issue',)  # Fields available for filtering

# Registering the Comments model with custom admin configuration
admin.site.register(Comments, ProjectComments)
