from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import DeviceSession

User = get_user_model()


class AuthEndpointsTestCase(APITestCase):
    """
    Comprehensive test suite for authentication endpoints.
    Covers positive, negative, edge, and error cases.
    """

    def setUp(self):
        """Set up test client and helper data."""
        self.client = APIClient()
        self.register_url = '/api/auth/register'
        self.login_url = '/api/auth/login'
        self.me_url = '/api/auth/me'
        self.logout_url = '/api/auth/logout'
        self.refresh_url = '/api/auth/refresh'
        self.sessions_url = '/api/auth/sessions'

        # Test user data
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'device_name': 'Test Device'
        }

    def create_user(self, email='test@example.com', name='Test User', password='testpass123'):
        """Helper method to create a test user."""
        user = User.objects.create_user(
            email=email, name=name, password=password)
        return user

    def get_tokens_for_user(self, user):
        """Helper method to generate access and refresh tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def authenticate_client(self, user=None):
        """Helper method to authenticate the test client with a user's tokens."""
        if not user:
            user = self.create_user()
        tokens = self.get_tokens_for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        return tokens

    def create_device_session(self, user, device_name='Test Device'):
        """Helper method to create a device session for a user."""
        refresh = RefreshToken.for_user(user)
        session = DeviceSession.objects.create(
            user=user,
            device_name=device_name,
            refresh_token_jti=str(refresh['jti'])
        )
        return session, str(refresh)

    # === REGISTER VIEW TESTS ===
    def test_register_success(self):
        """Test successful user registration."""
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']
                         ['email'], self.user_data['email'])

        # Verify user created
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

        # Verify device session created
        session = DeviceSession.objects.get(user=user)
        self.assertEqual(session.device_name, 'Registration Device')

    def test_register_missing_email(self):
        """Test registration with missing email."""
        data = self.user_data.copy()
        del data['email']
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        data = self.user_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        self.create_user()
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_short_password(self):
        """Test registration with password too short."""
        data = self.user_data.copy()
        data['password'] = '123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_with_device_name(self):
        """Test registration with custom device name."""
        data = self.user_data.copy()
        data['device_name'] = 'Custom Device'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_data['email'])
        session = DeviceSession.objects.get(user=user)
        self.assertEqual(session.device_name, 'Custom Device')

    # === LOGIN VIEW TESTS ===
    def test_login_success(self):
        """Test successful login."""
        self.create_user()
        response = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('session_id', response.data)
        self.assertIn('user', response.data)

        # Verify device session created
        user = User.objects.get(email=self.login_data['email'])
        session = DeviceSession.objects.filter(user=user).latest('created_at')
        self.assertEqual(session.device_name, 'Test Device')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        self.create_user()
        data = self.login_data.copy()
        data['password'] = 'wrongpass'
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_missing_email(self):
        """Test login with missing email."""
        data = self.login_data.copy()
        del data['email']
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_missing_password(self):
        """Test login with missing password."""
        data = self.login_data.copy()
        del data['password']
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """Test login with nonexistent user."""
        response = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_inactive_user(self):
        """Test login with inactive user."""
        user = self.create_user()
        user.is_active = False
        user.save()
        response = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    # === ME VIEW TESTS ===
    def test_me_authenticated(self):
        """Test getting user profile when authenticated."""
        user = self.create_user()
        self.authenticate_client(user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['name'], user.name)

    def test_me_unauthenticated(self):
        """Test getting user profile when unauthenticated."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # === LOGOUT VIEW TESTS ===
    def test_logout_success(self):
        """Test successful logout."""
        user = self.create_user()
        session, refresh_token = self.create_device_session(user)
        data = {'refresh': refresh_token}
        self.authenticate_client(user)
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data['detail'], 'Logged out successfully')

        # Verify session revoked
        session.refresh_from_db()
        self.assertTrue(session.revoked)

    def test_logout_missing_refresh_token(self):
        """Test logout with missing refresh token."""
        user = self.create_user()
        self.authenticate_client(user)
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Missing refresh token')

    def test_logout_invalid_refresh_token(self):
        """Test logout with invalid refresh token."""
        user = self.create_user()
        self.authenticate_client(user)
        data = {'refresh': 'invalid_token'}
        response = self.client.post(self.logout_url, data, format='json')
        # Still succeeds due to exception handling
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_unauthenticated(self):
        """Test logout when unauthenticated."""
        data = {'refresh': 'some_token'}
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # === SECURE TOKEN REFRESH VIEW TESTS ===
    def test_refresh_success(self):
        """Test successful token refresh."""
        user = self.create_user()
        session, refresh_token = self.create_device_session(user)
        data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        # Verify session updated
        session.refresh_from_db()
        self.assertFalse(session.revoked)

    def test_refresh_missing_token(self):
        """Test refresh with missing token."""
        response = self.client.post(self.refresh_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Missing refresh token')

    def test_refresh_revoked_session(self):
        """Test refresh with revoked session."""
        user = self.create_user()
        session, refresh_token = self.create_device_session(user)
        session.revoked = True
        session.save()
        data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Session revoked or invalid')

    def test_refresh_invalid_token(self):
        """Test refresh with invalid token."""
        data = {'refresh': 'invalid_token'}
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token')

    def test_refresh_nonexistent_session(self):
        """Test refresh with token not linked to any session."""
        refresh = RefreshToken.for_user(self.create_user())
        data = {'refresh': str(refresh)}
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Session revoked or invalid')

    # === SESSION LIST VIEW TESTS ===
    def test_sessions_list_authenticated(self):
        """Test listing sessions when authenticated."""
        user = self.create_user()
        self.create_device_session(user, 'Device 1')
        self.create_device_session(user, 'Device 2')
        self.authenticate_client(user)
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        device_names = [s['device_name'] for s in response.data]
        self.assertIn('Device 1', device_names)
        self.assertIn('Device 2', device_names)

    def test_sessions_list_unauthenticated(self):
        """Test listing sessions when unauthenticated."""
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sessions_list_empty(self):
        """Test listing sessions with no sessions."""
        user = self.create_user()
        self.authenticate_client(user)
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # === SESSION REVOKE VIEW TESTS ===
    def test_revoke_session_success(self):
        """Test revoking a specific session."""
        user = self.create_user()
        session, _ = self.create_device_session(user)
        self.authenticate_client(user)
        url = f'/api/auth/sessions/{session.id}/revoke'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Session revoked')
        session.refresh_from_db()
        self.assertTrue(session.revoked)

    def test_revoke_session_not_found(self):
        """Test revoking a nonexistent session."""
        user = self.create_user()
        self.authenticate_client(user)
        fake_uuid = '12345678-1234-5678-9012-123456789012'
        url = f'/api/auth/sessions/{fake_uuid}/revoke'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Session not found')

    def test_revoke_other_user_session(self):
        """Test revoking another user's session (should fail)."""
        user1 = self.create_user('user1@example.com')
        user2 = self.create_user('user2@example.com')
        session, _ = self.create_device_session(user1)
        self.authenticate_client(user2)
        url = f'/auth/sessions/{session.id}/revoke'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        session.refresh_from_db()
        self.assertFalse(session.revoked)

    def test_revoke_session_unauthenticated(self):
        """Test revoking session when unauthenticated."""
        user = self.create_user()
        session, _ = self.create_device_session(user)
        url = f'/api/auth/sessions/{session.id}/revoke'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
