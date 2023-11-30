from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.users_list),
    path('users/<int:id>', views.users_list_detail),
]
