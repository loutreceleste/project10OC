from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UsersViewset
from projects.views import ProjectViewSet, ContributorViewSet, IssuesViewSet, CommentsViewSet


router = routers.SimpleRouter()

router.register('users', UsersViewset, basename='users')
router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributors')
router.register('issues', IssuesViewSet, basename='issues')
router.register('comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/projects/<int:project_id>/contributors/', ContributorViewSet.as_view({'get': 'list'}), name='project-contributors'),
    path('api/projects/<int:project_id>/issues/', IssuesViewSet.as_view({'get': 'list'}), name='project-issues'),
    path('api/contributors/<int:project_id>/projects/', ProjectViewSet.as_view({'get': 'list'}), name='contributors-project'),

]
