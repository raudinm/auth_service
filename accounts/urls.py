from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    SessionListView,
    SessionRevokeView,
    SecureTokenRefreshView,
)

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/refresh", SecureTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/sessions", SessionListView.as_view(), name="sessions"),
    path("auth/sessions/<uuid:pk>/revoke",
         SessionRevokeView.as_view(), name="session_revoke"),
]
