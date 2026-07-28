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

	def __str__(self):
		return self.user.username  # ty:ignore[unresolved-attribute]
