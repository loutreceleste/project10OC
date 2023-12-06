from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models

class Project(models.Model):
    class Type(models.TextChoices):
        BACK_END = "BE", _("Back-end")
        FRONT_END = "FE", _("Front-end")
        IOS = "IO", _("IOs")
        ANDRIOD = "AN", _("Android")

    type = models.CharField(max_length=2, choices=Type.choices, default=None)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True)
    contributors = models.ManyToManyField('Contributor', related_name='projects_contributed', blank=True)
    name = models.fields.CharField(max_length=100, unique=True)
    description = models.fields.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributions', on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, related_name='contributors_assigned', on_delete=models.CASCADE)

class Issues(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_author', on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)



