from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire.")
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire.")
        user = self.model(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User (AbstractBaseUser, PermissionsMixin):
    username = models.fields.CharField(max_length=100, unique=True)
    can_be_contacted = models.BooleanField(default=False, verbose_name="Peut etre contacté")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Peut etre partagé")
    birthday = models.DateField(verbose_name="Date d'anniversaire", null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def age(self):

        if self.birthday:
            return int((datetime.date.today() - self.birthday).days // 365.25)
        else:
            return None

    USERNAME_FIELD = 'username'
