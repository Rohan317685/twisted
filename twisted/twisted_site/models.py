import martor.extensions
from django.contrib.auth import get_user_model
from django.db import models
from . import hackatime
from martor.models import MartorField

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verification_status = models.CharField(max_length=64, blank=True, default="")
    slack_id = models.CharField(max_length=64, blank=True, default="")
    slack_username = models.CharField(max_length=64, blank=True, default="")
    slack_pfp_url = models.CharField(max_length=200, blank=True, default="")

    hackatime_access_token = models.CharField(max_length=2000, blank=True, default="")
    hackatime_state = models.CharField(max_length=100, blank=True, default="")
    
    def __str__(self):
        return self.user.username  # ty:ignore[unresolved-attribute]


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="projects")

    project_name = models.CharField(max_length=50)
    project_description = models.TextField(max_length=2000)
    
    project_type = models.CharField(choices={'software': 'Software', 'hardware': 'Hardware'}, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    hackatime_project_name = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.project_name

    def get_hackatime_project(self) -> hackatime.HackatimeProject | None:
        if not self.hackatime_project_name:
            return
        projects = hackatime.projects(self.user.profile.hackatime_access_token)
        for project in projects:
            if project.name == self.hackatime_project_name:
                return project
        return
    
    def time_logged(self):
        minutes = 0
        for journal in self.journals.all():  # ty:ignore[unresolved-attribute]
            # django-orm-lens-disable-next-line DOL007
            minutes += journal.minutes_worked
        return minutes
    
    def time_spent(self):
        project = self.get_hackatime_project()
        if project is None:
            return 0
        return project.total_seconds / 60

class Journal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="journals")
    
    content = MartorField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    minutes_worked = models.IntegerField()
    
    def __str__(self):
        return f"{self.minutes_worked} mins on {self.project}"