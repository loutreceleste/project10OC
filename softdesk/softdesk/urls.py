from django.contrib import admin
from django.urls import path, include

from ressources.views import ProjectViewSet, ProjectsIssuesViewSet, IssuesCommentsViewSet, ProjectsContributorsViewSet
from authentication.views import UsersViewset

from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', UsersViewset, basename='users')
router.register('projects', ProjectViewSet, basename='all-project')

nested_router_project = NestedSimpleRouter(router, r'projects', lookup='project')
nested_router_project.register(r'issues', ProjectsIssuesViewSet, basename='project-issues')
nested_router_project.register(r'contributors', ProjectsContributorsViewSet, basename='project-contributors')

nested_router_issue = NestedSimpleRouter(nested_router_project, r'issues', lookup='issue')
nested_router_issue.register(r'comments', IssuesCommentsViewSet, basename='project-issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(router.urls)),
    path('api/', include(nested_router_project.urls)),
    path('api/', include(nested_router_issue.urls)),
]

