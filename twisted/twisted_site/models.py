from attr.validators import max_len
from django.contrib.auth import get_user_model
from django.db import models

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
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField(max_length=2000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

    def new_journal(self, content):
        Journal.objects.create(project=self)  # ty:ignore[unresolved-attribute]

class Journal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    
    content = models.TextField(max_length=2000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    minutes_worked = models.IntegerField()
    
    def __str__(self):
        return f"{self.minutes_worked} mins on {self.project}"