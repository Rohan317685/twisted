from .views.client.auth import LoginView, AuthCallbackView, HackatimeCallbackView, LogoutView
from django.urls import path
from .views import client
from .views.misc import upload_file

urlpatterns = [
    path('', view=client.HomepageView.as_view(), name="homepage"),
    path('faqs/', view=client.FaqsView.as_view(), name="faqs"),

    path("api/upload_image/", upload_file, name="misc.upload_file"),
    
    path("auth/login/", LoginView.as_view(), name="login"),
    path("oauth/callback/", AuthCallbackView.as_view(), name="auth_callback"),
    path("oauth/hackatime_callback/", HackatimeCallbackView.as_view(), name="auth_callback"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    
    path("dashboard/", client.DashboardView.as_view(), name="dashboard"),
    path("dashboard/frame/projects/", client.ListProjects.as_view(), name="fr.projects"),
    path("dashboard/frame/projects/create/", client.CreateProject.as_view(), name="fr.projects.create"),

    path("dashboard/frame/projects/<int:id>/", client.ProjectDetail.as_view(), name="fr.projects.detail"),
    path("dashboard/frame/projects/<int:id>/settings/", client.ProjectSettings.as_view(), name="fr.projects.settings"),
    path("dashboard/frame/projects/<int:id>/journals/new/hackatime/", client.NewProjectHackatimeJournal.as_view(), name="fr.projects.journals.new.hackatime"),
    path("dashboard/frame/projects/<int:id>/journals/new/lookout/", client.NewProjectLookoutJournal.as_view(), name="fr.projects.journals.new.lookout"),
    path("dashboard/frame/projects/<int:id>/journals/new/untracked/", client.NewProjectUntrackedJournal.as_view(), name="fr.projects.journals.new.untracked"),

]
