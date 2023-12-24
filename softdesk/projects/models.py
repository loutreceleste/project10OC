import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models

# Model representing a Project
class Project(models.Model):
    # Choices for different types of projects
    class Type(models.TextChoices):
        BACK_END = "BE", _("Back-end")
        FRONT_END = "FE", _("Front-end")
        IOS = "IO", _("IOs")
        ANDROID = "AN", _("Android")

    # Fields for the Project model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=2, choices=Type.choices, default=None)
    name = models.fields.CharField(max_length=100, unique=True)
    description = models.fields.CharField(max_length=500)

    # String representation of the Project model
    def __str__(self):
        return self.name

# Model representing an Issue related to a Project
class Issues(models.Model):
    # Choices for priority, nature, and progression of issues
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

    # Fields for the Issues model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issue_author', on_delete=models.CASCADE,
                               editable=False, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    projects = models.ForeignKey(Project, related_name='issue_project', on_delete=models.CASCADE, default=None,
                                 null=True)
    name = models.fields.CharField(max_length=100, unique=True, default=None)
    description = models.fields.CharField(max_length=500, default=None)
    comments = models.ManyToManyField('Comments', related_name='issue_comments', blank=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='issue_contributors', blank=True)

    priority = models.CharField(max_length=2, choices=Priority.choices, default=None)
    nature = models.CharField(max_length=2, choices=Nature.choices, default=None)
    progression = models.CharField(max_length=2, choices=Progression.choices, default=Progression.TO_DO)

# Model representing Comments on Issues
class Comments(models.Model):
    # Fields for the Comments model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author', on_delete=models.CASCADE,
                               editable=False, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    issue = models.ForeignKey(Issues, related_name='comment_issue', on_delete=models.CASCADE, default=None, null=True)
    description = models.fields.CharField(max_length=500, default=None)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

# Model representing Contributors for Projects
class Contributor(models.Model):
    # Fields for the Contributor model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributor_author', on_delete=models.CASCADE,
                               editable=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributor_user', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    projects = models.ForeignKey(Project, related_name='contributor_projects', blank=True, on_delete=models.CASCADE)
