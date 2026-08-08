from django.urls import path
from . import views

app_name = "slack_bot"

urlpatterns = [
    path("events", views.slack_events, name="events"),
]
