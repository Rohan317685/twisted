from django.db import models

# Create your models here.
class SupportMember(models.Model):
    user_id=models.CharField(max_length=200, unique=True)
    is_admin=models.BooleanField()
    
    def __str__(self):
        return f"{self.user_id} {'(admin)' if self.is_admin else ''}"
