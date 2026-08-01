from .views.client.auth import LoginView, AuthCallbackView, HackatimeCallbackView, LogoutView
from django.urls import path
from .views.client.homepage import HomepageView, FaqsView
from .views.client.dashboard import DashboardView
from .views.client.projects import ListProjects, CreateProject
from .views.client.project import ProjectDetail, ProjectSettings

urlpatterns = [
    path('', view=HomepageView.as_view(), name="homepage"),
    path('faqs/', view=FaqsView.as_view(), name="faqs"),
    
    path("auth/login/", LoginView.as_view(), name="login"),
    path("oauth/callback/", AuthCallbackView.as_view(), name="auth_callback"),
    path("oauth/hackatime_callback/", HackatimeCallbackView.as_view(), name="auth_callback"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/frame/projects/", ListProjects.as_view(), name="fr.projects"),
    path("dashboard/frame/projects/create/", CreateProject.as_view(), name="fr.projects.create"),

    path("dashboard/frame/projects/<int:id>/", ProjectDetail.as_view(), name="fr.projects.detail"),
    path("dashboard/frame/projects/<int:id>/settings/", ProjectSettings.as_view(), name="fr.projects.settings"),
]
