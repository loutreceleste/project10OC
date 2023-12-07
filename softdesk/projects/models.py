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
    contributors = models.ManyToManyField('Contributor', related_name='project_contributors', blank=True)
    name = models.fields.CharField(max_length=100, unique=True)
    description = models.fields.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Issues(models.Model):
    class Priority(models.TextChoices):
        LOW = "LO", _("Low")
        MEDIUM = "ME", _("Medium")
        HIGH = "HI", _("High")

    class Nature(models.TextChoices):
        BUG = "BU", _("Bug")
        FEATURE = "FE", _("Feature")
        TASK = "TA", _("Task")

    class Progression(models.TextChoices):
        TO_DO = "TD", _("To-Do")
        IN_PROGRESS = "IP", _("In progress")
        FINISHED = "FI", _("Finished")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_author', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    projects = models.ForeignKey(Project, related_name='issue_project', on_delete=models.CASCADE, default=None, null=True)

    name = models.fields.CharField(max_length=100, unique=True, default=None)
    description = models.fields.CharField(max_length=500, default=None)
    contributor = models.ForeignKey('Contributor', related_name='issue_contributor', on_delete=models.CASCADE, default=None, null=True)

    priority = models.CharField(max_length=2, choices=Priority.choices, default=None)
    nature = models.CharField(max_length=2, choices=Nature.choices, default=None)
    progression = models.CharField(max_length=2, choices=Progression.choices, default=Progression.TO_DO)

class Comment (models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    projects = models.ForeignKey(Project, related_name='comment_projects', on_delete=models.CASCADE, default=None, null=True)

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributor_user', on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, related_name='contributor_projects', blank=True)
    issues = models.ManyToManyField(Issues, related_name='contributor_issues', blank=True)
    comments = models.ManyToManyField(Comment, related_name='contributor_comments', blank=True)





