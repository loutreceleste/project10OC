from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User (AbstractBaseUser):
    username = models.fields.CharField(max_length=100, unique=True)
    can_be_contacted = models.BooleanField(default=False, verbose_name="Peut etre contacté")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Peut etre partagé")
    birthday = models.DateField(verbose_name="Date d'anniversaire")
    created_time = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    projects = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='Projects',
        related_name='projet',
        blank=True,
    )

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days // 365.25)

    USERNAME_FIELD = 'username'
