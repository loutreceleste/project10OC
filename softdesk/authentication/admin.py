from django.contrib import admin
from .models import User

class AuthenticationUser(admin.ModelAdmin):
    list_display = ('username', 'birthday', 'last_login', 'age')
    search_fields = ('username',)

admin.site.register(User, AuthenticationUser)

