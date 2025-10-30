from django.utils import timezone
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from .models import DeviceSession
from .serializers import RegisterSerializer, UserSerializer, DeviceSessionSerializer


# === USER REGISTRATION ===
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Registers a new user and returns JWT tokens immediately.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        device_name = request.data.get("device_name", "Registration Device")

        refresh = RefreshToken.for_user(user)
        jti = str(refresh["jti"])
        DeviceSession.objects.create(
            user=user, device_name=device_name, refresh_token_jti=jti)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


# === LOGIN ===
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        device_name = request.data.get("device_name", "Unknown Device")

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {
                    "detail": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        jti = str(refresh["jti"])
        device_session = DeviceSession.objects.create(
            user=user, device_name=device_name, refresh_token_jti=jti
        )

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "session_id": str(device_session.id),
                "user": UserSerializer(user).data,
            }
        )


# === GET CURRENT USER PROFILE ===
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns the authenticated user's profile information.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# === GOOGLE AUTH (OAUTH2) ===
class GoogleAuthView(SocialLoginView):
    """
    Handles Google OAuth2 login using dj-rest-auth + allauth.
    Frontend must send 'access_token' obtained from Google Sign-In.
    """
    adapter_class = GoogleOAuth2Adapter


# === LOGOUT ===
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logs out the user by revoking the current refresh token.
        If the blacklist app is enabled, the token is also blacklisted.
        """
        refresh_token = request.data.get("refresh")

        # Validate param from request
        if not refresh_token:
            return Response({"detail": "Missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            jti = token["jti"]
            DeviceSession.objects.filter(
                refresh_token_jti=jti).update(revoked=True)
            token.blacklist()  # optional, requires SIMPLEJWT blacklist app
        except Exception:
            pass
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)


# === LIST ALL ACTIVE SESSIONS ===
class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns all device sessions associated with the authenticated user.
        """
        sessions = DeviceSession.objects.filter(user=request.user)
        serializer = DeviceSessionSerializer(sessions, many=True)
        return Response(serializer.data)


# === REVOKE A SPECIFIC SESSION ===
class SessionRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Revokes a specific device session by marking it as 'revoked'.
        """
        try:
            session = DeviceSession.objects.get(id=pk, user=request.user)
        except DeviceSession.DoesNotExist:
            return Response({"detail": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        session.revoked = True
        session.save()
        return Response({"detail": "Session revoked"}, status=status.HTTP_200_OK)


# === TOKEN REFRESH WITH SESSION CONTROL ===
class SecureTokenRefreshView(TokenRefreshView):
    """
    Extends the default SimpleJWT TokenRefreshView.
    Validates that the refresh token belongs to a valid, non-revoked session.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            jti = token["jti"]
            ds = DeviceSession.objects.filter(refresh_token_jti=jti).first()
            if not ds or ds.revoked:
                return Response({"detail": "Session revoked or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

            # Proceed with the normal refresh process
            response = super().post(request, *args, **kwargs)

            # If refresh token rotation is used, update the stored JTI
            if response.status_code == 200:
                new_refresh = response.data.get("refresh")
                if new_refresh:
                    new_jti = str(RefreshToken(new_refresh)["jti"])
                    ds.refresh_token_jti = new_jti
                    ds.last_seen = timezone.now()
                    ds.save()

            return response

        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
