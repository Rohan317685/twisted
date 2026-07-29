from django.contrib import admin
from .models import Profile, Project, Journal

# Register your models here.
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Journal)
