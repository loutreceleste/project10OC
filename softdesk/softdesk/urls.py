from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UsersViewset
from projects.views import ProjectViewSet, ContributorViewSet


router = routers.SimpleRouter()

router.register('users', UsersViewset, basename='users')
router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributors')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
