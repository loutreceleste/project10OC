from django.contrib import admin
from .models import User

class AuthenticationUser(admin.ModelAdmin):
    # Customizes the display of the User model in Django admin.
    list_display = ('username', 'birthday', 'last_login', 'age')  # Fields displayed for each user
    search_fields = ('username',)  # Field(s) available for search

admin.site.register(User, AuthenticationUser)
