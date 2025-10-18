from pathlib import Path
from os import getenv, path
import cloudinary
from datetime import timedelta  

from dotenv import load_dotenv
# ======================================================================
# PROJECT DIRECTORY STRUCTURE
# ======================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root of the Django project (where manage.py lives)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# APPS_DIR points to where our custom Django apps are stored
# This allows for organized separation of core functionality
APPS_DIR = BASE_DIR / 'core_apps'

# ======================================================================
# ENVIRONMENT CONFIGURATION
# ======================================================================

# Load environment variables from .env.local file if it exists
# This provides a secure way to store sensitive configuration data
# Environment variables are loaded early to be available throughout settings
local_env_file = path.join(BASE_DIR, '.envs', '.env.local')
if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ======================================================================
# APPLICATION DEFINITION - Modular App Architecture
# ======================================================================

# Core Django applications required for basic functionality
# These provide essential features like admin, auth, sessions, etc.
DJANGO_APPS = [
    'django.contrib.admin',        # Admin interface for content management
    'django.contrib.auth',         # Authentication and authorization system
    'django.contrib.contenttypes', # Content type framework for generic relations
    'django.contrib.sessions',     # Session framework for user state
    'django.contrib.messages',     # Messaging framework for user feedback
    'django.contrib.staticfiles',  # Static file management (CSS, JS, images)
    'django.contrib.sites'         # Multi-site framework for domain handling
]

# Third-party packages that extend Django functionality
# Each package provides specific features for the real estate platform
THIRD_PARTY_APPS = [
    'rest_framework',      # Django REST Framework for API development
    'django_countries',    # Country field with validation for property locations
    'phonenumber_field',   # International phone number validation and formatting
    'drf_spectacular',     # OpenAPI 3.0 schema generation for API documentation
    'djoser',             # REST authentication endpoints (login, register, etc.)
    'social_django',      # Social authentication (Google, Facebook, etc.)
    'taggit',             # Tagging system for properties and posts
    'djcelery_email',     # Celery-based email sending for asynchronous notifications
    'cloudinary',         # Cloud-based image storage and transformation
    'django_celery_beat', # Periodic task scheduling with database persistence
]

# Custom Django applications specific to the real estate domain
# Each app handles a specific aspect of the business logic
LOCAL_APPS = [
    'core_apps.users',    # Custom user model and user management
    'core_apps.profiles', # User profiles with additional information
    'core_apps.ratings',  # Rating and review system for properties/agents
    'core_apps.common',   # Shared models and utilities across apps
    'core_apps.issues',   # Issue reporting and tracking system
    'core_apps.posts',    # Property listings and blog posts
    'core_apps.apartments', # Apartment-specific models and logic
    'core_apps.reports',  # Reputation tenants field. Report other tenants.
]
 
# Complete list of installed applications
# Django processes apps in this order for migrations and discovery
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ======================================================================
# MIDDLEWARE CONFIGURATION - Request/Response Processing Pipeline
# ======================================================================

# Middleware classes process requests and responses in order
# Each middleware provides specific security or functionality features
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',    # Security headers and HTTPS enforcement
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling for user state
    'django.middleware.common.CommonMiddleware',        # Common operations (URL normalization, etc.)
    'django.middleware.csrf.CsrfViewMiddleware',       # CSRF protection for forms and API
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Message framework support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
]

# ======================================================================
# URL CONFIGURATION
# ======================================================================

# Root URL configuration module
# Points to the main URLs file that defines all application routes
ROOT_URLCONF = 'config.urls'

# ======================================================================
# TEMPLATE CONFIGURATION
# ======================================================================

# Template engine configuration for rendering HTML
# Primarily used for admin interface and any server-rendered pages
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / 'templates')],  # Custom template directory
        'APP_DIRS': True,  # Look for templates in each app's templates/ directory
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Access to request object
                'django.contrib.auth.context_processors.auth', # Access to user object
                'django.contrib.messages.context_processors.messages',  # Access to messages
            ],
        },
    },
]

# ======================================================================
# WSGI APPLICATION
# ======================================================================

# WSGI application object for deployment
# Used by web servers (nginx, Apache) to serve the Django application
WSGI_APPLICATION = 'config.wsgi.application'

# ======================================================================
# DATABASE CONFIGURATION - PostgreSQL Setup
# ======================================================================

# Database configuration using environment variables for security
# PostgreSQL is chosen for its robust features needed in real estate:
# - JSONB fields for flexible property data
# - Full-text search capabilities
# - Geospatial extensions for location-based queries
# - Strong consistency and ACID compliance
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB'),       # Database name from environment
        'USER': getenv('POSTGRES_USER'),     # Database user from environment
        'PASSWORD': getenv('POSTGRES_PASSWORD'),  # Database password from environment
        'HOST': getenv('POSTGRES_HOST'),     # Database host (container name in Docker)
        'PORT': getenv('POSTGRES_PORT'),     # Database port (usually 5432)
    }
}

# ======================================================================
# PASSWORD SECURITY CONFIGURATION
# ======================================================================

# Password hashing algorithms in order of preference
# Argon2 is the most secure and recommended by Django
# Other hashers provide backward compatibility and security layers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",     # Most secure (default)
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",     # Django's previous default
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher", # Backward compatibility
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher", # bcrypt variant
    "django.contrib.auth.hashers.ScryptPasswordHasher",     # Memory-hard function
]

# Password validation rules to ensure strong user passwords
# These validators check various aspects of password security
AUTH_PASSWORD_VALIDATORS = [
    {
        # Prevents passwords too similar to user information
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Enforces minimum password length (default: 8 characters)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Prevents commonly used passwords (password123, etc.)
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Prevents purely numeric passwords
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ======================================================================
# INTERNATIONALIZATION AND LOCALIZATION
# ======================================================================

# Default language for the application
# Can be overridden per-user or per-request
LANGUAGE_CODE = 'en-us'

# Default timezone for the application
# Africa/Nairobi chosen for target market (Kenya real estate)
TIME_ZONE = 'Africa/Nairobi'

# Enable Django's internationalization framework
# Allows for multi-language support in the future
USE_I18N = True

# Enable timezone-aware datetime handling
# Critical for accurate timestamps across different time zones
USE_TZ = True

# Site framework configuration
# Required for certain Django features and third-party packages
SITE_ID = 1

# ======================================================================
# STATIC FILES CONFIGURATION
# ======================================================================

# URL prefix for static files (CSS, JavaScript, images)
STATIC_URL = '/static/'

# Directory where collected static files are stored. Nginx serves these files directly in production for better performance
# Used by 'python manage.py collectstatic' command
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# ======================================================================
# MODEL CONFIGURATION
# ======================================================================

# Default primary key field type for new models
# BigAutoField provides larger ID space for high-volume applications
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure django-taggit for case-insensitive tags
# Allows for better user experience when tagging properties
TAGGIT_CASE_INSENSITIVE = True

# Custom user model for extended user functionality
# Allows for additional fields and methods specific to real estate users
AUTH_USER_MODEL = 'users.User'

# ======================================================================
# API DOCUMENTATION CONFIGURATION - DRF Spectacular
# ======================================================================

# OpenAPI/Swagger documentation settings
# Provides interactive API documentation for developers and clients
SPECTACULAR_SETTINGS = {
    'TITLE': 'Alpha Apartments API',
    'DESCRIPTION': 'An Apartment Management API for Real Estate',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,  # Don't include schema in the served API
    'CONTACT': {
        'email': 'bernadx90@gmail.com'  # API maintainer contact
    },
    'LICENSE': {
        'name': 'MIT License'  # API license information
    },
}

# ======================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ======================================================================

# Django REST Framework configuration for API functionality
# Sets up schema generation for automatic documentation
REST_FRAMEWORK = {
    # Use drf-spectacular's AutoSchema for OpenAPI 3.0 compatibility
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ======================================================================
# CELERY CONFIGURATION - Asynchronous Task Processing
# ======================================================================

# Set Celery timezone to match Django timezone for consistency
# Ensures scheduled tasks run at expected times
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

# Redis configuration for Celery message broker and result backend
# Redis provides fast, reliable message queuing for asynchronous tasks
CELERY_BROKER_URL = getenv('CELERY_BROKER_URL')        
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND') 

# Celery serialization settings for security and compatibility
# JSON serialization is safer than pickle and more portable
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_TASK_SERIALIZER = 'json'              
CELERY_RESULT_SERIALIZER = 'json'            

# Result backend reliability settings
# Ensures task results are stored reliably even if Redis is temporarily unavailable
CELERY_RESULT_BACKEND_MAX_RETRIES = 10    
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True 

# Task execution monitoring and events
# Enables monitoring of task execution for debugging and metrics
CELERY_TASK_SEND_SENT_EVENT = True    
CELERY_WORKER_EXTENDED = True       #  enables the task result attributes, that is, the name arguments, keyword arguments, workers retries and delivery info to be written to the backend.
CELERY_WORKER_SEND_TASK_EVENTS = True 

# Task execution time limits
# Prevents runaway tasks from consuming resources indefinitely
CELERY_TASK_TIME_LIMIT = 300      
CELERY_TASK_SOFT_TIME_LIMIT = 60  



# Configure celery beat to use the database scheduler provided by the Django celery
# beat package.And this database scheduler stores the schedule in the Django database, allowing you to dynamically
# add, edit, and remove periodic tasks through the Django admin interface or through the Django models.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_WORKER_SEND_TASK_EVENTS = True #send task related events to the backend

CELERY_BEAT_SCHEDULE = {
    'update_reputations_every_day': {
        'task': 'update_all_reputations',        
    }
}

CLOUDINARY_CLOUD_NAME= getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY= getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET= getenv("CLOUDINARY_API_SECRET")
cloudinary.config( 
  cloud_name = CLOUDINARY_CLOUD_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET,
  
)

COOKIE_NAME="access"
COOKIE_SAMESITE="Lax"
COOKIE_PATH="/"
COOKIE_HTTPONLY=True
COOKIE_SECURE=getenv("COOKIE_SECURE", "True")=="True"


REST_FRAMEWORK ={
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core_apps.common.cookie_auth.CookieJWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",    
    "PAGE_SIZE": 10,
    
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        
    ],
    
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/day",
        "user": "1000/day",
    },
}

SIMPLE_JWT = {
    "SIGNING_KEY": getenv("SIGNING_KEY"),
     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
     "ROTATE_REFRESH_TOKENS": True,
     "USER_ID_FIELD": "id",
     "USER_ID_CLAIM": "user_id",
}

DJOSER = { 
          "USER_ID_FIELD": "id", 
          "LOGIN_FIELD": "email", 
          "TOKEN_MODEL": None, 
          "USER_CREATE_PASSWORD_RETYPE": True,
          "SEND_ACTIVATION_EMAIL": True,
          "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
          "PASSWORD_RESET_CONFIRM_RETYPE": True,
          "ACTIVATION_URL": "activate/{uid}/{token}",
          "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
          
          "SERIALIZERS": {
              "user_create": "core_apps.users.serializers.CreateUserSerializer",
              "current_user": "core_apps.users.serializers.CustomUserSerializer",
          },
          "PERMISSIONS": {
              "user": ["djoser.permissions.CurrentUserOrAdmin"],
              "user_list": ["rest_framework.permissions.IsAuthenticated"],
          },
}
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = getenv("REDIRECT_URIS", "").split(",")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "core_apps.profiles.pipeline.save_profile",  # Custom pipeline to save profile
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",  # Google OAuth2 backend
    "django.contrib.auth.backends.ModelBackend",  # Default Django auth backend
]

