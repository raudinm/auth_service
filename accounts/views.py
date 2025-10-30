from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import DeviceSession
from django.contrib.auth import authenticate


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        device_name = request.data.get('device_name', 'unknown')
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        # Save device session and store refresh token jti
        jti = str(refresh['jti'])
        ds = DeviceSession.objects.create(
            user=user, device_name=device_name, refresh_token_jti=jti)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'session_id': str(ds.id),
        }
        return Response(data)
