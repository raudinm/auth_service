from django.urls import path
from .views import (
    MeView,
    LoginView,
    LogoutView,
    RegisterView,
    GoogleAuthView,
    SessionListView,
    SessionRevokeView,
    SecureTokenRefreshView,
)

urlpatterns = [
    path("auth/register", RegisterView.as_view(), name="register"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/me", MeView.as_view(), name="me"),
    path("auth/refresh", SecureTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/sessions", SessionListView.as_view(), name="sessions"),
    path("auth/sessions/<uuid:pk>/revoke",
         SessionRevokeView.as_view(), name="session_revoke"),
    path("auth/google", GoogleAuthView.as_view(), name="google_login"),
]
