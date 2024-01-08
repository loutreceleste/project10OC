from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime

# Custom User Manager for managing user creation
class UserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")

        # Validate age if birthday is provided
        if 'birthday' in extra_fields:
            birthday_date = datetime.strptime(extra_fields['birthday'], '%Y-%m-%d').date()

            today = datetime.now().date()
            age_limit = today.replace(year=today.year - 15)

            if birthday_date > age_limit:
                raise ValueError("User must be at least 15 years old.")

        # Set default fields and create the user
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # Method to create a superuser
    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")

        # Set birthday as None for a superuser
        extra_fields['birthday'] = None

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create and save the superuser
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Custom User model with necessary fields and methods
class User(AbstractBaseUser, PermissionsMixin):
    username = models.fields.CharField(max_length=100, unique=True)
    can_be_contacted = models.BooleanField(default=False, verbose_name="Can be contacted")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Can data be shared")
    birthday = models.DateField(verbose_name="Birthday")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()  # Assigning the custom UserManager to manage User objects

    def save(self, *args, **kwargs):
        # Convertir la chaîne 'birthday' en objet 'date' si elle est au format 'YYYY-MM-DD'
        if isinstance(self.birthday, str):
            self.birthday = datetime.strptime(self.birthday, '%Y-%m-%d').date()

        # Valider l'âge lors de l'enregistrement de l'instance utilisateur
        if self.birthday:
            today = datetime.now().date()
            age_limit = today.replace(year=today.year - 15)

            if self.birthday > age_limit:
                raise ValueError("User must be at least 15 years old.")

        super().save(*args, **kwargs)

    # Method to calculate and return the user's age
    def age(self):
        if self.birthday:
            current_date = datetime.now().date()
            days_passed = current_date - self.birthday
            years_passed = days_passed.days // 365.25
            return int(years_passed)
        else:
            return None

    USERNAME_FIELD = 'username'  # Specifies the username field for authentication
