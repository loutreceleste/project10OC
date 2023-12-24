from django.contrib import admin
from django.urls import path, include
from projects.views import ProjectViewSet, ProjectsIssuesViewSet, IssuesCommentsViewSet, ProjectsContributorsViewSet
from authentication.views import UsersViewset
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

# Default router for the main API endpoints
router = routers.DefaultRouter()
router.register('users', UsersViewset, basename='users')  # Endpoint for managing users
router.register('projects', ProjectViewSet, basename='all-project')  # Endpoint for managing projects

# Nested router for projects to handle issues and contributors
nested_router_project = NestedSimpleRouter(router, r'projects', lookup='project')
nested_router_project.register(r'issues', ProjectsIssuesViewSet, basename='project-issues')  # Endpoint for managing project issues
nested_router_project.register(r'contributors', ProjectsContributorsViewSet, basename='project-contributors')  # Endpoint for managing project contributors

# Nested router for issues to handle comments
nested_router_issue = NestedSimpleRouter(nested_router_project, r'issues', lookup='issue')
nested_router_issue.register(r'comments', IssuesCommentsViewSet, basename='project-issue-comments')  # Endpoint for managing issue comments

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL

    path('api-auth/', include('rest_framework.urls')),  # URL patterns for Django Rest Framework authentication views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token-based authentication
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint

    path('api/', include(router.urls)),  # Main API endpoints for users and projects
    path('api/', include(nested_router_project.urls)),  # Nested API endpoints for issues and contributors within projects
    path('api/', include(nested_router_issue.urls)),  # Nested API endpoints for comments within issues
]
