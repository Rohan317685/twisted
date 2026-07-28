from .views.client.auth import LoginView, AuthCallbackView, LogoutView
from django.urls import path
from .views.client.homepage import HomepageView
from .views.client.dashboard import DashboardView

urlpatterns = [
    path('', view=HomepageView.as_view(), name="homepage"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("oauth/callback/", AuthCallbackView.as_view(), name="auth_callback"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

]
