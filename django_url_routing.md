  DJANGO URL ROUTING - COMPLETE EXPLANATION

  ---
  1. HOW DJANGO URL ROUTING WORKS (The Hierarchy)

  When a request comes in (e.g., POST http://localhost/api/v1/auth/login/), Django does this:

  1. Django reads ROOT_URLCONF setting → points to config.urls
  2. Django loads config/urls.py and checks urlpatterns
  3. Django tries to match the URL path against each pattern IN ORDER
  4. If pattern uses include(), Django:
     - Strips the matched portion
     - Loads the included URL file
     - Continues matching with remaining path
  5. When final match found → calls the view

  ---
  2. YOUR URL HIERARCHY - COMPLETE MAPPING

  Let me trace every authentication URL:

  Level 1: Root URLs (config/urls.py)

  # config/urls.py (lines 20-23)
  urlpatterns = [
      path("api/v1/auth/", include("djoser.urls")),           # Line 20
      path("api/v1/auth/", include("djoser.urls.jwt")),       # Line 21
      path("api/v1/auth/", include("core_apps.users.urls")),  # Line 22
      path("api/v1/auth/", include("social_django.urls", namespace="social")),  # Line 23
  ]

  Key Point: All 4 include() statements start with "api/v1/auth/". When a request comes in with that prefix, Django strips it and passes the remaining path to each
  included URL file.

  ---
  Level 2: What Each Include Provides

  Let me map EVERY URL that gets created:

  ---
  A. include("djoser.urls") → djoser/urls/base.py

  This uses Django REST Framework's DefaultRouter which auto-generates multiple URLs:

  # djoser/urls/base.py (lines 6-7)
  router = DefaultRouter()
  router.register("users", views.UserViewSet)

  Generated URLs:

  | Full URL                                   | HTTP Method | View                               | Purpose                  |
  |--------------------------------------------|-------------|------------------------------------|--------------------------|
  | /api/v1/auth/users/                        | GET         | UserViewSet.list                   | List all users (admin)   |
  | /api/v1/auth/users/                        | POST        | UserViewSet.create                 | Register new user        |
  | /api/v1/auth/users/me/                     | GET         | UserViewSet.me                     | Get current user details |
  | /api/v1/auth/users/me/                     | PUT/PATCH   | UserViewSet.me                     | Update current user      |
  | /api/v1/auth/users/me/                     | DELETE      | UserViewSet.me                     | Delete current user      |
  | /api/v1/auth/users/{id}/                   | GET         | UserViewSet.retrieve               | Get specific user        |
  | /api/v1/auth/users/{id}/                   | PUT/PATCH   | UserViewSet.update                 | Update specific user     |
  | /api/v1/auth/users/{id}/                   | DELETE      | UserViewSet.destroy                | Delete specific user     |
  | /api/v1/auth/users/activation/             | POST        | UserViewSet.activation             | Activate account         |
  | /api/v1/auth/users/resend_activation/      | POST        | UserViewSet.resend_activation      | Resend activation email  |
  | /api/v1/auth/users/set_password/           | POST        | UserViewSet.set_password           | Change password          |
  | /api/v1/auth/users/reset_password/         | POST        | UserViewSet.reset_password         | Request password reset   |
  | /api/v1/auth/users/reset_password_confirm/ | POST        | UserViewSet.reset_password_confirm | Confirm password reset   |
  | /api/v1/auth/users/set_username/           | POST        | UserViewSet.set_username           | Change username          |
  | /api/v1/auth/users/reset_username/         | POST        | UserViewSet.reset_username         | Request username reset   |
  | /api/v1/auth/users/reset_username_confirm/ | POST        | UserViewSet.reset_username_confirm | Confirm username reset   |

  ---
  B. include("djoser.urls.jwt") → djoser/urls/jwt.py

  # djoser/urls/jwt.py (lines 4-8)
  urlpatterns = [
      re_path(r"^jwt/create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
      re_path(r"^jwt/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
      re_path(r"^jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
  ]

  Generated URLs:

  | Full URL                  | HTTP Method | View                | Purpose                                    |
  |---------------------------|-------------|---------------------|--------------------------------------------|
  | /api/v1/auth/jwt/create/  | POST        | TokenObtainPairView | Login with email/password (get JWT tokens) |
  | /api/v1/auth/jwt/refresh/ | POST        | TokenRefreshView    | Refresh access token                       |
  | /api/v1/auth/jwt/verify/  | POST        | TokenVerifyView     | Verify if token is valid                   |

  Note: You're NOT using these! You override them with your custom views below.

  ---
  C. include("core_apps.users.urls") → core_apps/users/urls.py

  # core_apps/users/urls.py (lines 6-14)
  urlpatterns = [
      re_path(
          r"^o/(?P<provider>\S+)/$",
          CustomProviderAuthView.as_view(),
          name="provider-auth"
      ),
      path("login/", CustomTokenObtainPairView.as_view()),
      path("refresh/", CustomTokenRefreshView.as_view()),
      path("logout/", LogoutView.as_view(), name="logout"),
  ]

  Generated URLs:

  | Full URL                       | HTTP Method | View                      | Purpose                               |
  |--------------------------------|-------------|---------------------------|---------------------------------------|
  | /api/v1/auth/o/google-oauth2/  | POST        | CustomProviderAuthView    | Social auth (Google OAuth2)           |
  | /api/v1/auth/o/facebook/       | POST        | CustomProviderAuthView    | Social auth (Facebook)                |
  | /api/v1/auth/o/<any-provider>/ | POST        | CustomProviderAuthView    | Social auth (any provider)            |
  | /api/v1/auth/login/            | POST        | CustomTokenObtainPairView | Login (email/password) - YOUR VERSION |
  | /api/v1/auth/refresh/          | POST        | CustomTokenRefreshView    | Refresh token - YOUR VERSION          |
  | /api/v1/auth/logout/           | POST        | LogoutView                | Logout (clear cookies)                |

  Key Point: The regex r"^o/(?P<provider>\S+)/$" captures any provider name in the URL.
  - o/google-oauth2/ → matches, provider="google-oauth2"
  - o/facebook/ → matches, provider="facebook"
  - o/github/ → matches, provider="github"

  ---
  D. include("social_django.urls", namespace="social") → social_django/urls.py

  # social_django/urls.py (lines 12-23)
  urlpatterns = [
      path(f"login/<str:backend>/", views.auth, name="begin"),
      path(f"complete/<str:backend>/", views.complete, name="complete"),
      path(f"disconnect/<str:backend>/", views.disconnect, name="disconnect"),
      path(f"disconnect/<str:backend>/<int:association_id>/",
           views.disconnect, name="disconnect_individual"),
  ]

  Generated URLs:

  | Full URL                               | HTTP Method | View                           | Purpose                  |
  |----------------------------------------|-------------|--------------------------------|--------------------------|
  | /api/v1/auth/login/google-oauth2/      | GET         | social_django.views.auth       | Redirect to Google login |
  | /api/v1/auth/complete/google-oauth2/   | GET         | social_django.views.complete   | OAuth callback handler   |
  | /api/v1/auth/disconnect/google-oauth2/ | POST        | social_django.views.disconnect | Unlink Google account    |

  Important: These are the traditional social-auth-app-django URLs. You're NOT using these for OAuth because you're using Djoser's CustomProviderAuthView instead
  (which handles it via API POST, not redirect callbacks).

  ---
  3. URL CONFLICTS & RESOLUTION

  Question: Why don't login/ and refresh/ conflict?

  # Djoser provides:
  /api/v1/auth/jwt/create/      # from djoser.urls.jwt
  /api/v1/auth/jwt/refresh/     # from djoser.urls.jwt

  # You override with:
  /api/v1/auth/login/           # from core_apps.users.urls
  /api/v1/auth/refresh/         # from core_apps.users.urls

  Answer: They're different URLs! Django matches /api/v1/auth/login/ FIRST (because core_apps.users.urls is included in line 22, AFTER djoser in line 21), but the
  paths are different (login/ vs jwt/create/).

  Django's matching order in config/urls.py:
  1. Line 20: Try djoser.urls paths first
  2. Line 21: Try djoser.urls.jwt paths
  3. Line 22: Try core_apps.users.urls paths ← Your custom views
  4. Line 23: Try social_django.urls paths

  Since your paths (login/, refresh/) don't match djoser's paths (jwt/create/, jwt/refresh/), there's no conflict.

  ---
  4. COMPLETE URL MAP - ALL AUTHENTICATION ENDPOINTS

● Here's what you actually use:

  ✅ ACTIVE ENDPOINTS (what you'll use):

  Registration & Account Management:
    POST   /api/v1/auth/users/                    → Register new user
    POST   /api/v1/auth/users/activation/         → Activate account
    POST   /api/v1/auth/users/reset_password/     → Request password reset
    POST   /api/v1/auth/users/reset_password_confirm/  → Confirm reset
    GET    /api/v1/auth/users/me/                 → Get current user

  Email/Password Authentication:
    POST   /api/v1/auth/login/                    → Login (CustomTokenObtainPairView)
    POST   /api/v1/auth/refresh/                  → Refresh token (CustomTokenRefreshView)
    POST   /api/v1/auth/logout/                   → Logout (LogoutView)

  Social Authentication:
    POST   /api/v1/auth/o/google-oauth2/          → Google OAuth (CustomProviderAuthView)
    POST   /api/v1/auth/o/facebook/               → Facebook OAuth (if configured)

  ❌ NOT USED (provided but overridden):
    POST   /api/v1/auth/jwt/create/               → Djoser's login (you use /login/ instead)
    POST   /api/v1/auth/jwt/refresh/              → Djoser's refresh (you use /refresh/ instead)
    
  ❌ NOT USED (social-django traditional flow):
    GET    /api/v1/auth/login/google-oauth2/      → Redirect-based OAuth (old way)
    GET    /api/v1/auth/complete/google-oauth2/   → OAuth callback (old way)

  ---
  5. REDIRECT URIs - THE CONFUSION EXPLAINED

  You have this in your .env:
  REDIRECT_URIS="http://localhost:8080/api/v1/auth/google,http://localhost/api/v1/auth/complete/google-oauth2/"

  Let me explain what each one is for:

  ---
  A. http://localhost:8080/api/v1/auth/google (Frontend URL)

  This is your FRONTEND callback URL. Here's the flow:

  1. Frontend redirects user to Google:
     https://accounts.google.com/o/oauth2/v2/auth?
       client_id=YOUR_CLIENT_ID
       &redirect_uri=http://localhost:8080/api/v1/auth/google  ← THIS ONE
       &response_type=code
       &scope=openid email profile
       &state=RANDOM

  2. User approves on Google

  3. Google redirects BACK to your frontend:
     http://localhost:8080/api/v1/auth/google?code=4/0AVGzR...&state=RANDOM

  4. Your frontend (Next.js) receives the code

  5. Frontend sends code to your BACKEND:
     POST http://localhost/api/v1/auth/o/google-oauth2/
     Body: code=4/0AVGzR...&state=RANDOM&redirect_uri=http://localhost:8080/api/v1/auth/google

  Important: When you send the code to your backend, you MUST include the same redirect_uri that Google used. This is a security check by Google.

  ---
  B. http://localhost/api/v1/auth/complete/google-oauth2/ (Backend URL - NOT USED)

  This is the traditional social-django callback URL. This would be used if you were doing server-side OAuth redirects (the old way):

  Old Flow (you're NOT using this):
  1. User clicks "Login with Google"
  2. Backend redirects to Google:
     GET /api/v1/auth/login/google-oauth2/  → social_django redirects to Google
  3. User approves
  4. Google redirects to:
     GET /api/v1/auth/complete/google-oauth2/?code=...  ← social_django handles it
  5. Backend processes code and redirects to frontend

  You don't need this because you're using Djoser's API-based flow (CustomProviderAuthView), not redirect-based flow.

  ---
  C. What SOCIAL_AUTH_ALLOWED_REDIRECT_URIS Does

  # config/settings/base.py:384
  SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = getenv("REDIRECT_URIS", "").split(",")

  This setting tells python-social-auth (the library behind social-django and Djoser's social auth) which redirect URIs are allowed. It's a security measure to
  prevent redirect attacks.

  In your case:
  - http://localhost:8080/api/v1/auth/google → Frontend callback (USED)
  - http://localhost/api/v1/auth/complete/google-oauth2/ → Backend callback (NOT USED, but allowed for safety)

  ---
  6. GOOGLE OAUTH CONFIGURATION

  You also need to configure these redirect URIs in Google Cloud Console:

  1. Go to https://console.cloud.google.com/
  2. Navigate to: APIs & Services → Credentials
  3. Click on your OAuth 2.0 Client ID
  4. Under "Authorized redirect URIs", add:
  http://localhost:8080/api/v1/auth/google
  http://localhost/api/v1/auth/google

  ---
  7. SERIALIZERS - HOW THEY FIT IN

● Serializers handle data validation and transformation between JSON and Python objects.

  # core_apps/users/serializers.py
  class CreateUserSerializer(UserCreateSerializer):
      class Meta(UserCreateSerializer.Meta):
          model = User
          fields = ['id', 'username', 'first_name', 'last_name', 'password']

  Where this is used:

  # config/settings/base.py:376-378
  DJOSER = {
      "SERIALIZERS": {
          "user_create": "core_apps.users.serializers.CreateUserSerializer",  ← HERE
      },
  }

  Request Flow:

  POST /api/v1/auth/users/
  Body: {
    "username": "john",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "pass123",
    "re_password": "pass123"
  }

  ↓ Django routes to UserViewSet.create (from djoser.urls)

  ↓ UserViewSet looks up serializer from settings:
    DJOSER["SERIALIZERS"]["user_create"] → CreateUserSerializer

  ↓ CreateUserSerializer validates data:
    • Checks all required fields present
    • Validates password strength (Django validators)
    • Checks password == re_password
    • Validates email format

  ↓ If valid: serializer.save() creates User object in database

  ↓ Serializer converts User object back to JSON for response

  ↓ Response: {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }  # password NOT included (security)

  Why customize it?

  # Djoser's default UserCreateSerializer includes:
  fields = ['email', 'username', 'password']

  # Your custom serializer adds:
  fields = ['id', 'username', 'first_name', 'last_name', 'password']
           ↑ added     ↑ added           ↑ added

  So users can provide first/last name during registration.

  ---
  8. COMPLETE FLOW DIAGRAM

  REQUEST: POST /api/v1/auth/o/google-oauth2/
           Body: code=4/0AVG...&state=xxx&redirect_uri=http://localhost:8080/api/v1/auth/google

           ↓

  ┌────────────────────────────────────────────────────────────────┐
  │ 1. Django reads ROOT_URLCONF → config.urls                     │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 2. Checks urlpatterns in config/urls.py:                       │
  │    Line 20: path("api/v1/auth/", include("djoser.urls"))       │
  │       → No match (djoser has users/, not o/google-oauth2/)     │
  │    Line 21: path("api/v1/auth/", include("djoser.urls.jwt"))   │
  │       → No match (djoser.jwt has jwt/create/, not o/...)       │
  │    Line 22: path("api/v1/auth/", include("core_apps.users..."))│
  │       → MATCH! Strips "api/v1/auth/" → remaining: "o/google-oauth2/" │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 3. Loads core_apps/users/urls.py, checks urlpatterns:          │
  │    re_path(r"^o/(?P<provider>\S+)/$", CustomProviderAuthView)  │
  │       → MATCH! provider="google-oauth2"                        │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 4. Calls CustomProviderAuthView.post()                         │
  │    (from core_apps/users/views.py:114)                         │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 5. CustomProviderAuthView.post() calls:                        │
  │    provider_res = super().post(request, *args, **kwargs)       │
  │    → Calls parent ProviderAuthView.post() (from Djoser)        │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 6. Djoser's ProviderAuthView:                                  │
  │    • Validates state parameter                                 │
  │    • Extracts code & redirect_uri from request body            │
  │    • Uses social-core to exchange code for Google tokens       │
  │    • Calls Google API to get user info (email, name)           │
  │    • Checks if user exists in DB:                              │
  │      - Exists → Login                                          │
  │      - New → Create user (uses social pipeline)                │
  │    • Generates JWT access & refresh tokens                     │
  │    • Returns Response with tokens                              │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 7. Back in CustomProviderAuthView.post():                      │
  │    • Checks status == 201                                      │
  │    • Extracts tokens from response                             │
  │    • Calls set_auth_cookies(response, access, refresh)         │
  │    • Removes tokens from response body                         │
  │    • Returns response with cookies                             │
  └────────────────────────────────────────────────────────────────┘
           ↓
  ┌────────────────────────────────────────────────────────────────┐
  │ 8. Response sent to frontend:                                  │
  │    Headers:                                                     │
  │      Set-Cookie: access=eyJ0eXA...; HttpOnly; Secure           │
  │      Set-Cookie: refresh=eyJ0eXA...; HttpOnly; Secure          │
  │      Set-Cookie: logged_in=true                                │
  │    Body:                                                        │
  │      {"message": "Social login successful", "user": {...}}     │
  └────────────────────────────────────────────────────────────────┘

  ---

● SUMMARY - KEY TAKEAWAYS

  1. URL Hierarchy:
  config/urls.py (root)
    ├─ include("djoser.urls") → /users/, /users/activation/, etc.
    ├─ include("djoser.urls.jwt") → /jwt/create/, /jwt/refresh/ (not used)
    ├─ include("core_apps.users.urls") → /login/, /refresh/, /o/<provider>/
    └─ include("social_django.urls") → /complete/<backend>/ (not used)
  2. Redirect URIs:
    - http://localhost:8080/api/v1/auth/google → Frontend receives code from Google ✅ USED
    - http://localhost/api/v1/auth/complete/google-oauth2/ → Backend redirect handler ❌ NOT USED
  3. Serializers:
    - Validate & transform data between JSON ↔ Python objects
    - Configured in DJOSER["SERIALIZERS"]
    - Your custom one adds first_name, last_name, id to registration
  4. Your Custom Views:
    - Wrap library views to add cookie functionality
    - Inherit from parent, call super(), then add cookie logic
