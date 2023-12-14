from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UsersViewset
from projects.views import ProjectViewSet, ContributorViewSet, IssuesViewSet, CommentsViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()

router.register('users', UsersViewset, basename='users')
router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributors')
router.register('issues', IssuesViewSet, basename='issues')
router.register('comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),

    path('api/projects/<int:project_id>/contributors/', ProjectViewSet.as_view({'get': 'get_contributors'}), name='project_contributors'),
    path('api/projects/<int:project_id>/issues/', ProjectViewSet.as_view({'get': 'get_issues'}), name='project_issues'),

    path('api/issues/<int:issues_id>/comments/', IssuesViewSet.as_view({'get': 'get_comments'}), name='issues-comments'),
]
