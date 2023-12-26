from django.contrib import admin
from django.urls import path, include
from projects.views import ProjectViewSet, ProjectsIssuesViewSet, IssuesCommentsViewSet, ProjectsContributorsViewSet
from authentication.views import UsersViewset
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuring OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API Softdesk",
        default_version='v1',
        description="This API acts as a support for a secure and high-performing backend, designed within the framework of a ticket, issue, and comment system aimed at managing projects with contributor participation. It is intended to be used by various frontend applications across different platforms.",
        contact=openapi.Contact(email="edygaram@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Setting the API to be publicly accessible
    permission_classes=[permissions.AllowAny],  # Granting permission to all users without authentication
)

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

