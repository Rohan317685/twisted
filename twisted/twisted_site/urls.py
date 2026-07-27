from .views.client.auth import LoginView, AuthCallbackView
from django.urls import path
from .views.client.homepage import HomepageView

urlpatterns = [
    path('', view=HomepageView.as_view()),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("oauth/callback/", AuthCallbackView.as_view(), name="auth_callback"),
    # path("auth/logout/", logout_view, name="logout"),

]
