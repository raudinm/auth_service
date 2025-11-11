# Auth Service

This project provides a Django backend with Next.js frontend for authentication services, including JWT tokens, session management, and Google OAuth integration.

## Project Overview

The Auth Service is a comprehensive authentication system built with Django REST Framework (backend) and Next.js (frontend). It provides secure user authentication, session management, and social login integration with Google OAuth2. The system supports JWT-based authentication with refresh token rotation, device session tracking, and secure logout mechanisms.

The backend handles all authentication logic, user management, and session control, while the frontend provides a modern React-based interface for user interactions. The project includes extensive test coverage and CI/CD setup with GitHub Actions.

## Features

- **User Registration & Login**: Secure user registration with email/password and JWT token generation
- **JWT Authentication**: Access and refresh token-based authentication with automatic rotation
- **Device Session Management**: Track and manage user sessions across multiple devices
- **Secure Logout**: Token blacklisting and session revocation
- **Google OAuth2 Integration**: Social login with Google accounts
- **Session Control**: List active sessions and revoke specific sessions
- **Password Security**: Argon2 password hashing with validation
- **CORS Support**: Cross-origin resource sharing configuration
- **Comprehensive Testing**: 30+ test cases covering all endpoints and edge cases
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## Tech Stack

### Backend

- **Django 5.2.7**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **JWT (Simple JWT)**: Token-based authentication
- **Allauth**: Social authentication
- **Argon2**: Password hashing
- **CORS Headers**: Cross-origin support
- **WhiteNoise**: Static file serving
- **Pytest**: Testing framework

### Frontend

- **Next.js 15**: React framework
- **React 19**: UI library
- **NextAuth 4**: Authentication library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Hook Form**: Form handling

### DevOps

- **GitHub Actions**: CI/CD
- **PostgreSQL**: Database
- **SQLite**: Testing Database (Github Actions only)

## Prerequisites

- Python 3.11+
- Node.js 22+
- PostgreSQL 15+
- Git

## Installation and Setup

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone git@github.com:raudinm/auth_service.git
   cd auth_service
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and configure:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration (see Environment Variables section).

5. **Set up database:**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd nextjs-auth-client
   ```

2. **Install dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env.local`:

   ```bash
   cp .env.example .env.local
   ```

   Configure the variables (see Environment Variables section).

4. **Run the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)

```env
# Django Core
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000

# Database
DATABASE_NAME=auth_service_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# SSL/Security
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_SECRET=your-google-client-secret
```

### Frontend (.env.local)

```env
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Running the Application

1. **Start the backend:**

   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start the frontend:**

   ```bash
   cd nextjs-auth-client
   yarn dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin panel: http://localhost:8000/admin/

## Testing

### Test Overview

The project includes comprehensive test coverage with 30 test cases covering all authentication endpoints, including positive, negative, and edge cases.

### Detailed Test Cases for Each Endpoint

#### Registration Tests (6 cases)

1. **test_register_success**: Successful user registration with valid data
2. **test_register_missing_email**: Registration fails with missing email
3. **test_register_invalid_email**: Registration fails with invalid email format
4. **test_register_duplicate_email**: Registration fails with existing email
5. **test_register_short_password**: Registration fails with password too short
6. **test_register_with_device_name**: Registration succeeds with custom device name

#### Login Tests (6 cases)

7. **test_login_success**: Successful login with valid credentials
8. **test_login_invalid_credentials**: Login fails with wrong password
9. **test_login_missing_email**: Login fails with missing email
10. **test_login_missing_password**: Login fails with missing password
11. **test_login_nonexistent_user**: Login fails for non-existent user
12. **test_login_inactive_user**: Login fails for inactive user account

#### Profile Tests (2 cases)

13. **test_me_authenticated**: Retrieve user profile when authenticated
14. **test_me_unauthenticated**: Profile access fails when not authenticated

#### Logout Tests (4 cases)

15. **test_logout_success**: Successful logout with valid refresh token
16. **test_logout_missing_refresh_token**: Logout fails with missing token
17. **test_logout_invalid_refresh_token**: Logout handles invalid token gracefully
18. **test_logout_unauthenticated**: Logout fails when not authenticated

#### Token Refresh Tests (5 cases)

19. **test_refresh_success**: Successful token refresh with valid token
20. **test_refresh_missing_token**: Refresh fails with missing token
21. **test_refresh_revoked_session**: Refresh fails for revoked session
22. **test_refresh_invalid_token**: Refresh fails with invalid token
23. **test_refresh_nonexistent_session**: Refresh fails for token not linked to session

#### Session Management Tests (7 cases)

24. **test_sessions_list_authenticated**: List all user sessions when authenticated
25. **test_sessions_list_unauthenticated**: Session list access fails when not authenticated
26. **test_sessions_list_empty**: Return empty list when no sessions exist
27. **test_revoke_session_success**: Successfully revoke a specific session
28. **test_revoke_session_not_found**: Revoke fails for non-existent session
29. **test_revoke_other_user_session**: Cannot revoke another user's session
30. **test_revoke_session_unauthenticated**: Revoke fails when not authenticated

### Running Tests Locally

1. **Install test dependencies:**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run all tests:**

   ```bash
   python -m pytest test_endpoints.py -v
   ```

3. **Run with coverage:**

   ```bash
   python -m pytest test_endpoints.py --cov=. --cov-report=html
   ```

4. **Run specific test:**
   ```bash
   python -m pytest test_endpoints.py::AuthEndpointsTestCase::test_register_success -v
   ```

### GitHub Actions CI/CD

The project uses GitHub Actions for automated testing on every push and pull request to the main branch.

#### Workflow Configuration (.github/workflows/test.yml)

```yaml
name: Auth Service

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Endpoints
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r backend/requirements.txt

      - name: Run Django migrations
        run: |
          cd backend
          DJANGO_SETTINGS_MODULE=test_settings python manage.py migrate

      - name: Create staticfiles folder
        run: |
          cd backend
          mkdir staticfiles

      - name: Run tests
        run: DJANGO_SETTINGS_MODULE=test_settings python -m pytest backend/test_endpoints.py -v
```

#### Environment Variables for GitHub

No additional environment variables are required for the CI pipeline as tests use SQLite in-memory database.

### Running GitHub Actions Locally with act

You can test the GitHub Actions workflow locally using [act](https://github.com/nektos/act):

1. **Install act:**

   ```bash
   # macOS with Homebrew
   brew install act

   # Or download from releases
   ```

2. **Run the workflow:**

   ```bash
   act
   ```

3. **Run with specific event:**
   ```bash
   act push
   ```

## Google Authentication Integration

### Backend Google Auth Setup

1. **Install required packages:**
   Already included in `requirements.txt`:

   - `django-allauth`
   - `requests-oauthlib`

2. **Configure Django settings:**
   The settings are already configured in `auth_service/settings.py`:

   ```python
   INSTALLED_APPS = [
       # ... other apps
       'allauth',
       'allauth.account',
       'allauth.socialaccount',
       'allauth.socialaccount.providers.google',
   ]

   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.ModelBackend',
       'allauth.account.auth_backends.AuthenticationBackend',
   )

   ACCOUNT_AUTHENTICATION_METHOD = "email"
   ACCOUNT_EMAIL_REQUIRED = True
   ACCOUNT_USERNAME_REQUIRED = False
   ACCOUNT_USER_MODEL_USERNAME_FIELD = None
   ACCOUNT_UNIQUE_EMAIL = True
   ACCOUNT_EMAIL_VERIFICATION = "optional"

   AUTH_USER_MODEL = "accounts.User"
   ```

3. **Create Google OAuth credentials:**

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`

4. **Configure environment variables:**
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_SECRET=your-client-secret
   ```

### Frontend Google Auth Testing

The frontend uses NextAuth.js for Google OAuth integration.

1. **Configure NextAuth:**
   Already configured in `src/lib/auth.ts` with GoogleProvider.

2. **Set up Google OAuth in Google Cloud:**

   - Add authorized redirect URIs for frontend:
     - `http://localhost:3000/api/auth/callback/google`
     - `http://127.0.0.1:3000/api/auth/callback/google`

3. **Environment variables:**
   ```env
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Registering Google in Django Sites

1. **Access Django admin:**

   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/admin/
   ```

2. **Add site:**

   - Go to Sites → Sites
   - Change example.com to `localhost:8000` or your domain

3. **Add social application:**
   - Go to Social accounts → Social applications
   - Add new application:
     - Provider: Google
     - Name: Google OAuth
     - Client id: Your Google client ID
     - Secret key: Your Google client secret
     - Sites: Select your site

## API Endpoints Documentation

📘 **Postman Collection**: For testing the API endpoints, you can import the [`📘 Auth Service.postman_collection.json`](📘 Auth Service.postman_collection.json) file into Postman. It includes all authentication endpoints with example requests, proper headers, and variables for tokens.

### Authentication Endpoints

All endpoints are prefixed with `/api/auth/`

#### POST /api/auth/register

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "name": "User Name",
  "password": "securepassword123",
  "device_name": "My Device" // optional
}
```

**Response (201):**

```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

#### POST /api/auth/login

Authenticate user and return tokens.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "device_name": "My Device" // optional
}
```

**Response (200):**

```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi...",
  "session_id": "uuid-string",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

#### GET /api/auth/me

Get current user profile.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "User Name"
}
```

#### POST /api/auth/logout

Logout user and revoke session.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "refresh": "refresh_token_string"
}
```

**Response (205):**

```json
{
  "detail": "Logged out successfully"
}
```

#### POST /api/auth/refresh

Refresh access token.

**Request Body:**

```json
{
  "refresh": "refresh_token_string"
}
```

**Response (200):**

```json
{
  "access": "new_access_token"
}
```

#### GET /api/auth/sessions

List all active sessions for the user.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
[
  {
    "id": "uuid",
    "device_name": "My Device",
    "created_at": "2024-01-01T00:00:00Z",
    "last_seen": "2024-01-01T00:00:00Z",
    "revoked": false
  }
]
```

#### POST /api/auth/sessions/{session_id}/revoke

Revoke a specific session.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "detail": "Session revoked"
}
```

#### POST /api/auth/google

Authenticate with Google OAuth.

**Request Body:**

```json
{
  "access_token": "google_access_token",
  "device_name": "My Device" // optional
}
```

**Response (200):**

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "name": "User Name"
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run tests: `python -m pytest backend/test_endpoints.py -v`
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR
