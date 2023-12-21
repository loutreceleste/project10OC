from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime, timedelta

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire.")

        if 'birthday' in extra_fields:

            birthday_date = datetime.strptime(extra_fields['birthday'], '%Y-%m-%d').date()

            today = datetime.now().date()
            age_limit = today.replace(year=today.year - 15)

            if birthday_date > age_limit:
                raise ValueError("L'utilisateur doit avoir au moins 15 ans.")

        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire.")

        extra_fields['birthday'] = None

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User (AbstractBaseUser, PermissionsMixin):
    username = models.fields.CharField(max_length=100, unique=True)
    can_be_contacted = models.BooleanField(default=False, verbose_name="Peut etre contacté")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Peut etre partagé")
    birthday = models.DateField(verbose_name="Date d'anniversaire")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def age(self):

        if self.birthday:
            return int((datetime.date.today() - self.birthday).days // 365.25)
        else:
            return None

    USERNAME_FIELD = 'username'
