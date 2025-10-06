# Django Routing & OAuth Authentication - Anki Cards

## Django URL Routing Basics

### Card 1
**Q:** How does Django route an incoming HTTP request to the correct view?

**A:**
1. Django reads the `ROOT_URLCONF` setting (points to main urls.py)
2. Loads urlpatterns from that file
3. Tries to match the URL path against each pattern IN ORDER
4. If pattern uses `include()`, Django strips the matched portion and continues matching in the included file
5. When final match found, Django calls the corresponding view

Example: Request to `/api/v1/auth/login/`
- Matches `path("api/v1/auth/", include(...))`
- Strips `"api/v1/auth/"`, remaining is `"login/"`
- Continues matching in included urls file

---

### Card 2
**Q:** What is the difference between `path()` and `include()` in Django urlpatterns?

**A:**
- **`path(route, view)`** - Maps a URL pattern directly to a view function/class
  ```python
  path("login/", LoginView.as_view())
  ```

- **`include(module)`** - Delegates URL matching to another urls.py file
  ```python
  path("api/v1/auth/", include("djoser.urls"))
  ```

When `include()` matches, Django strips that prefix and passes the remaining path to the included urlpatterns.

---

### Card 3
**Q:** Why can you have multiple `include()` statements with the same prefix in Django urlpatterns? Won't they conflict?

**A:**
No conflict! Django tries each included urlpattern file in order. If no match in first, tries second, etc.

```python
urlpatterns = [
    path("api/v1/auth/", include("djoser.urls")),        # has users/, activation/
    path("api/v1/auth/", include("djoser.urls.jwt")),    # has jwt/create/, jwt/refresh/
    path("api/v1/auth/", include("core_apps.users.urls")),  # has login/, logout/
]
```

Request to `/api/v1/auth/login/`:
1. Djoser.urls → No "login/" pattern → continue
2. Djoser.urls.jwt → No "login/" pattern → continue
3. core_apps.users.urls → Has "login/" → MATCH!

---

### Card 4
**Q:** What does Django's `re_path()` do and how is it different from `path()`?

**A:**
- **`path()`** - Simple string matching with angle brackets for parameters
  ```python
  path("users/<int:id>/", view)
  ```

- **`re_path()`** - Uses regex patterns for complex matching
  ```python
  re_path(r"^o/(?P<provider>\S+)/$", view)
  ```

`re_path()` allows:
- Named regex groups: `(?P<provider>\S+)` captures provider name
- Complex patterns: `\S+` matches any non-whitespace
- More control over URL structure

---

## Django REST Framework URL Patterns

### Card 5
**Q:** How does Django REST Framework's `DefaultRouter` generate URLs from a ViewSet?

**A:**
```python
router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = router.urls
```

Auto-generates these URLs:
- `GET/POST /users/` → list, create
- `GET/PUT/PATCH/DELETE /users/{id}/` → retrieve, update, destroy
- `GET/PUT/PATCH/DELETE /users/me/` → custom action
- `POST /users/activation/` → @action decorated methods

Each HTTP method on the same URL maps to different ViewSet methods.

---

### Card 6
**Q:** In Django, what determines the ORDER that URL patterns are checked against incoming requests?

**A:**
Django checks patterns in **top-to-bottom order** as defined in urlpatterns list.

```python
urlpatterns = [
    path("api/v1/auth/", include("djoser.urls")),      # Checked FIRST
    path("api/v1/auth/", include("core_apps.users.urls")),  # Checked SECOND
]
```

**Important:**
- First match wins
- More specific patterns should come before general ones
- Order matters when patterns could match the same URL

---

## OAuth2 Flow & URLs

### Card 7
**Q:** What are the THREE main URLs involved in Google OAuth2 authentication, and what is each one's purpose?

**A:**
1. **Google's authorization URL** (https://accounts.google.com/o/oauth2/v2/auth)
   - Where user sees consent screen
   - Returns authorization code

2. **Frontend callback URL** (http://localhost:8080/api/v1/auth/google)
   - Where Google redirects after user approves
   - Frontend receives the code

3. **Backend API endpoint** (POST /api/v1/auth/o/google-oauth2/)
   - Frontend sends code here
   - Backend exchanges code for user data & tokens

---

### Card 8
**Q:** In OAuth2 flow, what is the `redirect_uri` parameter and why must it be included twice?

**A:**
`redirect_uri` is the URL where OAuth provider sends the authorization code.

**Used twice for security:**

1. **When requesting code from Google:**
   ```
   https://accounts.google.com/o/oauth2/v2/auth?
     redirect_uri=http://localhost:8080/api/v1/auth/google
   ```

2. **When exchanging code for token:**
   ```
   POST /api/v1/auth/o/google-oauth2/
   Body: code=...&redirect_uri=http://localhost:8080/api/v1/auth/google
   ```

Google validates both match to prevent authorization code interception attacks.

---

### Card 9
**Q:** What does `SOCIAL_AUTH_ALLOWED_REDIRECT_URIS` setting control in Django social auth?

**A:**
It's a **whitelist** of allowed redirect URIs for OAuth callbacks.

```python
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = [
    "http://localhost:8080/api/v1/auth/google",
    "http://localhost/api/v1/auth/complete/google-oauth2/"
]
```

**Security purpose:**
- Prevents redirect attacks
- Only listed URIs can be used as OAuth callbacks
- Backend rejects requests with unlisted redirect_uri

If redirect_uri not in list → 400 Bad Request

---

### Card 10
**Q:** In the URL pattern `re_path(r"^o/(?P<provider>\S+)/$", CustomProviderAuthView)`, what does `(?P<provider>\S+)` do?

**A:**
It's a **named regex group** that captures the provider name from the URL.

**How it works:**
- `(?P<provider>...)` - Creates a named parameter called "provider"
- `\S+` - Matches one or more non-whitespace characters
- Value is passed to view as `kwargs["provider"]`

**Examples:**
- `/o/google-oauth2/` → provider="google-oauth2"
- `/o/facebook/` → provider="facebook"
- `/o/github/` → provider="github"

View accesses it: `self.kwargs["provider"]`

---

## Djoser URL Patterns

### Card 11
**Q:** What URLs does `include("djoser.urls")` provide in a Django REST API?

**A:**
Main authentication URLs from djoser/urls/base.py:

- `POST /users/` - Register new user
- `GET /users/me/` - Get current user
- `POST /users/activation/` - Activate account
- `POST /users/resend_activation/` - Resend activation email
- `POST /users/set_password/` - Change password
- `POST /users/reset_password/` - Request password reset
- `POST /users/reset_password_confirm/` - Confirm password reset
- `GET/PUT/PATCH/DELETE /users/{id}/` - User CRUD operations

Uses Django REST Framework's `DefaultRouter`.

---

### Card 12
**Q:** What's the difference between `include("djoser.urls")` and `include("djoser.urls.jwt")` in Django?

**A:**
- **`djoser.urls`** - User management endpoints (registration, activation, password reset)
  ```python
  POST /users/ - Register
  POST /users/activation/ - Activate
  ```

- **`djoser.urls.jwt`** - JWT token endpoints
  ```python
  POST /jwt/create/ - Login (get tokens)
  POST /jwt/refresh/ - Refresh access token
  POST /jwt/verify/ - Verify token validity
  ```

Both work together: djoser.urls handles accounts, djoser.urls.jwt handles authentication tokens.

---

### Card 13
**Q:** What does `include("social_django.urls", namespace="social")` provide in Django?

**A:**
Traditional social-auth-app-django redirect-based URLs:

```python
# From social_django/urls.py
GET  /login/<backend>/       - Redirect to OAuth provider
GET  /complete/<backend>/    - OAuth callback handler
POST /disconnect/<backend>/  - Unlink social account
```

**Example:**
- `GET /login/google-oauth2/` → Redirects to Google
- `GET /complete/google-oauth2/?code=...` → Handles callback

**Note:** These are OLD STYLE (server-side redirects). Modern APIs use Djoser's `ProviderAuthView` instead (API-based, no redirects).

---

## Authentication Backends

### Card 14
**Q:** What is the difference between `social_django` (in INSTALLED_APPS) and `GoogleOAuth2` (in AUTHENTICATION_BACKENDS)?

**A:**
**`social_django` (Django App)** - Infrastructure layer
- Provides database models (`UserSocialAuth`)
- Django integration utilities (`load_strategy`, `load_backend`)
- Storage for OAuth tokens
- Migrations for social auth tables

**`GoogleOAuth2` (Authentication Backend)** - OAuth logic layer
- Implements OAuth2 protocol
- Makes HTTP requests to Google APIs
- Exchanges codes for access tokens
- Extracts user data from Google
- Creates/updates Django users

**Analogy:** social_django is the car chassis, GoogleOAuth2 is the engine. You need both!

---

### Card 15
**Q:** Why does Django's `AUTHENTICATION_BACKENDS` have multiple backends, and how does Django choose which one to use?

**A:**
Multiple backends support different authentication methods:

```python
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",  # For Google OAuth
    "django.contrib.auth.backends.ModelBackend",  # For email/password
]
```

**Django tries each backend IN ORDER:**

1. **OAuth login:** `GoogleOAuth2.authenticate()` succeeds → returns user
2. **Email/password login:**
   - `GoogleOAuth2.authenticate()` fails → returns None
   - `ModelBackend.authenticate()` checks password → returns user

First backend to return a user wins. If all return None → authentication fails.

---

### Card 16
**Q:** What database table does `social_django` create, and what does it store?

**A:**
**Table:** `UserSocialAuth`

**Schema:**
```python
class UserSocialAuth(models.Model):
    user = ForeignKey(User)              # Links to Django user
    provider = CharField()               # "google-oauth2", "facebook"
    uid = CharField()                    # Provider's user ID
    extra_data = JSONField()             # OAuth tokens, profile data
    created = DateTimeField()
    modified = DateTimeField()
```

**Purpose:**
- Links Django users to social accounts (one user can have multiple social logins)
- Stores OAuth access/refresh tokens
- Tracks which provider authenticated the user

---

## OAuth Flow Implementation

### Card 17
**Q:** What are the 6 steps of the OAuth2 authorization code flow with a separate frontend/backend?

**A:**
1. **Frontend redirects user to Google**
   - URL: `https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...`

2. **User approves on Google consent screen**

3. **Google redirects to frontend callback**
   - URL: `http://localhost:8080/api/v1/auth/google?code=...&state=...`

4. **Frontend sends code to backend**
   - POST `/api/v1/auth/o/google-oauth2/` with code & state

5. **Backend exchanges code for user data**
   - Calls Google token endpoint
   - Gets user info from Google
   - Creates/logs in Django user

6. **Backend returns JWT tokens in cookies**
   - Frontend receives authentication cookies

---

### Card 18
**Q:** In Djoser's ProviderAuthView, what's the difference between GET and POST requests to `/api/v1/auth/o/google-oauth2/`?

**A:**
**GET Request** (optional):
```python
GET /api/v1/auth/o/google-oauth2/?redirect_uri=http://localhost:8080/...
Response: {"authorization_url": "https://accounts.google.com/..."}
```
- Returns Google's OAuth URL
- Frontend uses this to redirect user
- Alternative: frontend can build URL itself

**POST Request** (required):
```python
POST /api/v1/auth/o/google-oauth2/
Body: code=...&state=...&redirect_uri=...
Response: {"access": "jwt...", "refresh": "jwt...", "user": {...}}
```
- Receives authorization code from frontend
- Exchanges code for user data
- Returns JWT tokens

---

### Card 19
**Q:** What does `backend.auth_complete()` do in Django social auth, and what APIs does it call?

**A:**
`backend.auth_complete()` is the core OAuth method that:

1. **Extracts code** from request data
2. **Calls Google's token endpoint:**
   ```
   POST https://oauth2.googleapis.com/token
   Body: code=...&client_id=...&client_secret=...&redirect_uri=...
   Response: {"access_token": "ya29...", "expires_in": 3599}
   ```

3. **Calls Google's userinfo endpoint:**
   ```
   GET https://www.googleapis.com/oauth2/v2/userinfo
   Headers: Authorization: Bearer ya29...
   Response: {"email": "user@gmail.com", "name": "John Doe", ...}
   ```

4. **Creates/updates Django user** with email, name, etc.
5. **Saves OAuth association** in UserSocialAuth table
6. **Returns Django user object**

---

### Card 20
**Q:** When testing OAuth2 with Postman, what are the THREE required body parameters for `POST /api/v1/auth/o/google-oauth2/`?

**A:**
**Content-Type:** `application/x-www-form-urlencoded`

**Body parameters:**
1. **`code`** - Authorization code from Google (single-use, expires in ~60 seconds)
2. **`state`** - CSRF protection token (must match what was sent to Google)
3. **`redirect_uri`** - Must exactly match the URI used when requesting the code

**Example:**
```
code=4/0AVGzR1AOLoLlKpTe5OH...
state=9ti6NEfIxaK5e0exd4vR7hPU3MOU63G8
redirect_uri=http://localhost:8080/api/v1/auth/google
```

**Common mistake:** Putting these in URL query string instead of body → 404 error

---

## Serializers in Authentication

### Card 21
**Q:** What role do serializers play in Django REST Framework authentication, and when are they executed?

**A:**
Serializers handle **data validation and transformation** between JSON ↔ Python objects.

**Execution flow:**
1. **Request arrives** with JSON body
2. **View calls** `serializer = self.get_serializer(data=request.data)`
3. **Validation** `serializer.is_valid(raise_exception=True)` runs:
   - Checks required fields present
   - Validates field types and formats
   - Runs custom validation methods
4. **Saving** `serializer.save()` creates/updates database objects
5. **Response** serializer converts objects back to JSON

**Example:** `CreateUserSerializer` validates email format, password strength before creating user.

---

### Card 22
**Q:** How do you customize Djoser's user creation serializer, and why would you do this?

**A:**
**Configuration in settings.py:**
```python
DJOSER = {
    "SERIALIZERS": {
        "user_create": "core_apps.users.serializers.CreateUserSerializer",
    }
}
```

**Custom serializer:**
```python
class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password']
```

**Why customize:**
- Add fields (first_name, last_name) to registration
- Add custom validation logic
- Change password requirements
- Modify response format

Djoser's UserViewSet automatically uses the custom serializer.

---

### Card 23
**Q:** What does `ProviderAuthSerializer.validate()` do in Djoser's social authentication?

**A:**
```python
def validate(self, attrs):
    # 1. Validate CSRF state
    if "state" in request.GET:
        self._validate_state(request.GET["state"])

    # 2. Load OAuth backend
    strategy = load_strategy(request)
    backend = load_backend(strategy, "google-oauth2", redirect_uri=...)

    # 3. Complete OAuth flow
    user = backend.auth_complete()  # Calls Google APIs, gets user

    return {"user": user}
```

**Purpose:**
- CSRF protection (validates state parameter)
- Orchestrates OAuth code exchange
- Returns validated user for token generation

Runs before `create()` method generates JWT tokens.

---

## Custom Authentication Views

### Card 24
**Q:** Why create `CustomTokenObtainPairView` instead of using Django SimpleJWT's default `TokenObtainPairView`?

**A:**
**Default behavior:**
```python
# SimpleJWT returns tokens in response body
{"access": "eyJ0eXA...", "refresh": "eyJ0eXA..."}
```

**Custom behavior:**
```python
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Get tokens

        # Move tokens from body to HttpOnly cookies
        set_auth_cookies(response, access_token, refresh_token)
        response.data.pop("access")
        response.data.pop("refresh")

        return response
```

**Benefits:**
- Tokens in HttpOnly cookies → JavaScript can't access → XSS protection
- Cleaner API responses
- Automatic cookie handling by browser

---

### Card 25
**Q:** What's the difference between `CustomProviderAuthView` and `CustomTokenObtainPairView` in terms of what they inherit and when they're used?

**A:**
**`CustomProviderAuthView`** - Social (OAuth) login
```python
class CustomProviderAuthView(ProviderAuthView):  # Inherits from Djoser
    # Handles: POST /api/v1/auth/o/google-oauth2/
    # Flow: Receives OAuth code → exchanges for user → generates tokens
```

**`CustomTokenObtainPairView`** - Email/password login
```python
class CustomTokenObtainPairView(TokenObtainPairView):  # Inherits from SimpleJWT
    # Handles: POST /api/v1/auth/login/
    # Flow: Validates email/password → generates tokens
```

**Both do same thing:** Call parent for authentication logic, then add cookies to response.

---

### Card 26
**Q:** How does `CookieJWTAuthentication` authenticate requests in Django REST Framework?

**A:**
```python
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 1. Check Authorization header first
        if header := self.get_header(request):
            raw_token = self.get_raw_token(header)

        # 2. If no header, check cookies
        elif 'access' in request.COOKIES:
            raw_token = request.COOKIES.get('access')

        # 3. Validate token
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return (user, validated_token)
```

**Flow:**
- Tries header: `Authorization: Bearer token`
- Falls back to cookie: `Cookie: access=token`
- Returns authenticated user or None

---

## Testing & Debugging

### Card 27
**Q:** What are common mistakes when testing OAuth2 endpoint with Postman, and how do you fix them?

**A:**
**Mistake 1:** Putting parameters in URL
```
❌ POST /api/v1/auth/o/google-oauth2/?code=...&state=...
✅ POST /api/v1/auth/o/google-oauth2/
   Body: code=...&state=...
```

**Mistake 2:** Wrong Content-Type
```
❌ Content-Type in URL query string
✅ Headers: Content-Type: application/x-www-form-urlencoded
```

**Mistake 3:** Expired authorization code
```
❌ Using same code twice or after 60+ seconds
✅ Get fresh code from Google OAuth flow each time
```

**Mistake 4:** Mismatched redirect_uri
```
❌ Different redirect_uri than used with Google
✅ Exact match required: http://localhost:8080/api/v1/auth/google
```

---

### Card 28
**Q:** What must be configured in Google Cloud Console for OAuth2 to work with your Django backend?

**A:**
**In Google Cloud Console → APIs & Services → Credentials:**

1. **Create OAuth 2.0 Client ID**
   - Application type: Web application

2. **Authorized redirect URIs** (add both):
   ```
   http://localhost:8080/api/v1/auth/google
   http://localhost/api/v1/auth/google
   ```

3. **Copy credentials to Django settings:**
   ```python
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "your-client-id"
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "your-client-secret"
   ```

4. **Configure allowed redirect URIs in Django:**
   ```python
   SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = [
       "http://localhost:8080/api/v1/auth/google",
   ]
   ```

---

### Card 29
**Q:** What's the difference between these two redirect URIs in OAuth config: `http://localhost:8080/api/v1/auth/google` vs `http://localhost/api/v1/auth/complete/google-oauth2/`?

**A:**
**`http://localhost:8080/api/v1/auth/google`** ✅ USED
- **Frontend callback** (Next.js on port 8080)
- Where Google sends the authorization code
- Frontend receives code and sends to backend

**`http://localhost/api/v1/auth/complete/google-oauth2/`** ❌ NOT USED
- **Backend callback** (traditional social-django flow)
- Used for server-side redirect-based OAuth
- You're using API-based flow instead (Djoser's ProviderAuthView)

**Modern API approach:** Google → Frontend → Backend (what you're doing)
**Old approach:** Google → Backend → Frontend (traditional social-django)

---

### Card 30
**Q:** How do you trace a URL request through Django's routing system to find which view handles it?

**A:**
**Manual trace:**
1. Start with ROOT_URLCONF setting → `config.urls`
2. Check urlpatterns in order
3. Find first matching `path()` or `include()`
4. If `include()`, load that file and repeat with remaining path
5. Final match → that's your view

**Example: POST /api/v1/auth/o/google-oauth2/**
```python
# config/urls.py
path("api/v1/auth/", include("core_apps.users.urls"))  # Match!
  → Strip "api/v1/auth/", remaining: "o/google-oauth2/"

# core_apps/users/urls.py
re_path(r"^o/(?P<provider>\S+)/$", CustomProviderAuthView)  # Match!
  → provider="google-oauth2"
  → View: CustomProviderAuthView
```

**Debug tools:**
- Django Debug Toolbar (shows URL resolution)
- `django-extensions`: `python manage.py show_urls`

---

## Complete Flow Cards

### Card 31
**Q:** Trace the complete request/response cycle for email/password login with cookie-based JWT authentication.

**A:**
1. **Request:** `POST /api/v1/auth/login/`
   ```json
   {"email": "user@example.com", "password": "pass123"}
   ```

2. **Routing:** config/urls.py → core_apps/users/urls.py → CustomTokenObtainPairView

3. **View calls parent:** TokenObtainPairView validates credentials, generates JWT tokens

4. **Custom logic:** Extract tokens from response, call `set_auth_cookies()`

5. **Response:**
   ```
   Headers:
     Set-Cookie: access=eyJ0eXA...; HttpOnly; Secure
     Set-Cookie: refresh=eyJ0eXA...; HttpOnly; Secure
   Body:
     {"message": "Login successful"}
   ```

6. **Next request:** Browser auto-sends cookies → `CookieJWTAuthentication` validates → user authenticated

---

### Card 32
**Q:** Trace the complete OAuth2 flow from "user clicks Login with Google" to "user authenticated in Django backend".

**A:**
1. **Frontend:** User clicks button → Redirect to Google OAuth URL
   ```
   https://accounts.google.com/o/oauth2/v2/auth?
     client_id=...&redirect_uri=http://localhost:8080/api/v1/auth/google
   ```

2. **Google:** User approves → Redirect with code
   ```
   http://localhost:8080/api/v1/auth/google?code=...&state=...
   ```

3. **Frontend:** Extract code → POST to backend
   ```
   POST /api/v1/auth/o/google-oauth2/
   Body: code=...&state=...&redirect_uri=...
   ```

4. **Backend (CustomProviderAuthView):**
   - Validates state (CSRF protection)
   - Calls `backend.auth_complete()`
   - Exchanges code for Google access token
   - Gets user info from Google
   - Creates/logs in Django user
   - Generates JWT tokens
   - Sets cookies

5. **Response:** Cookies + user data → User authenticated

---

### Card 33
**Q:** What happens when an authenticated user makes a request to a protected Django REST Framework endpoint?

**A:**
1. **Request:** `GET /api/v1/protected/`
   ```
   Cookie: access=eyJ0eXAiOiJKV1QiLCJhbGc...
   ```

2. **DRF calls authentication classes** (from REST_FRAMEWORK settings):
   ```python
   DEFAULT_AUTHENTICATION_CLASSES = [
       "core_apps.common.cookie_auth.CookieJWTAuthentication"
   ]
   ```

3. **CookieJWTAuthentication.authenticate():**
   - Checks Authorization header (not present)
   - Checks 'access' cookie (found!)
   - Validates JWT signature
   - Checks expiration
   - Gets user from token's user_id claim
   - Returns `(user, token)`

4. **DRF checks permissions:**
   - `IsAuthenticated` → user is not None → Pass

5. **View executes** with `request.user` populated

6. **Response** returned to client

---

