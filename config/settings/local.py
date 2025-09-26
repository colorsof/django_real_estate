"""
======================================================================
DJANGO LOCAL DEVELOPMENT SETTINGS
======================================================================

PURPOSE:
This module contains Django settings specifically configured for local
development environments. It inherits from base.py and overrides or
adds development-specific configurations including:
- Debug mode enablement for detailed error pages
- Local database and email configuration
- Development-friendly security settings
- Enhanced logging for debugging
- Custom admin URL configuration for security

INHERITANCE PATTERN:
local.py → base.py (imports all base settings then overrides as needed)

ENVIRONMENT SETUP:
This file expects a .envs/.env.local file containing environment variables
for local development. Key variables include:
- DJANGO_SECRET_KEY: Cryptographic key for Django security
- DJANGO_ADMIN_URL: Custom admin interface URL path
- Database connection parameters
- Email service configuration
- Site domain and URL settings

SECURITY CONSIDERATIONS:
- DEBUG=True is ONLY for development - never use in production
- Secret key should be unique per environment
- CSRF protection configured for local development ports
- Admin URL can be customized for basic security through obscurity

USAGE:
Set DJANGO_SETTINGS_MODULE=config.settings.local in your environment
or when running Django management commands:
python manage.py runserver --settings=config.settings.local

DEVELOPMENT WORKFLOW:
- Provides detailed error pages with full stack traces
- Enables Django Debug Toolbar integration (if added)
- Configures console logging for real-time debugging
- Allows all localhost variants for flexible development
======================================================================
"""

from os import getenv, path
from dotenv import load_dotenv

# Import all settings from base configuration
# This provides the foundation that local settings build upon
from .base import *  # noqa

from .base import BASE_DIR

# ======================================================================
# ENVIRONMENT VARIABLE LOADING
# ======================================================================

# Load local development environment variables
# This file should contain sensitive development data not in version control
local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# ======================================================================
# DEBUG AND DEVELOPMENT SETTINGS
# ======================================================================

# Enable debug mode for local development
# Provides detailed error pages, enhanced logging, and development tools
# WARNING: NEVER set DEBUG=True in production environments
DEBUG = True

# Site name for branding and notifications
# Used in email templates, page titles, and admin interface
SITE_NAME = getenv('SITE_NAME')

# ======================================================================
# SECURITY CONFIGURATION - Development Settings
# ======================================================================

# Django secret key for cryptographic signing
# Used for session signatures, CSRF tokens, password reset tokens, etc.
# Falls back to a development key if environment variable not set
SECRET_KEY = getenv(
    'DJANGO_SECRET_KEY',
    'rgJ4KsiINJjcmp-vBC8s2Kmvcw8Sh9oCRIuh6F-qUgyZGC3VbGE'  # Development fallback
)

# CSRF trusted origins for cross-origin requests
# Allows API calls from the local development server through nginx proxy
# Port 8080 matches the nginx proxy configuration in docker-compose
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

# Allowed hosts for Django to serve requests
# Includes all common localhost variants for development flexibility
ALLOWED_HOSTS = [
    'localhost',    # Standard localhost
    '127.0.0.1',   # IPv4 loopback
    '0.0.0.0'      # All interfaces (for Docker container access)
]

# ======================================================================
# ADMIN INTERFACE CONFIGURATION
# ======================================================================

# Custom admin URL configuration for security through obscurity
# Reads from environment variable and normalizes the format
_raw_admin = getenv('DJANGO_ADMIN_URL') or 'admin/'  # Default to 'admin/' if not set
_admin_stripped = _raw_admin.strip('/')  # Remove leading/trailing slashes

# Ensure admin URL always ends with slash for proper Django routing
# Example: 'supersecret' becomes 'supersecret/'
ADMIN_URL = f"{_admin_stripped}/"

# Configure login URL to match custom admin URL
# Ensures Django redirects unauthenticated users to correct admin login
LOGIN_URL = f"/{_admin_stripped}/login/"

# ======================================================================
# EMAIL CONFIGURATION - Development Settings
# ======================================================================

# Use Celery for asynchronous email sending
# Allows email sending without blocking web requests
# In development, emails are captured by Mailpit service
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

# Email server configuration from environment variables
# In local development, these point to the Mailpit SMTP server
EMAIL_HOST = getenv('EMAIL_HOST')        # Usually 'mailpit' (Docker service name)
EMAIL_PORT = getenv('EMAIL_PORT')        # Usually '1025' for Mailpit

# Default sender email address for system notifications
# Used for password resets, account confirmations, etc.
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')

# Domain name for generating absolute URLs in emails and redirects
# Important for proper link generation in email templates
DOMAIN = getenv('DOMAIN')

# ======================================================================
# LOGGING CONFIGURATION - Enhanced Development Logging
# ======================================================================

# Comprehensive logging configuration for development debugging
# Provides detailed console output for troubleshooting and development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Keep other loggers active
    
    # Log output handlers - where log messages are sent
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Output to console/terminal
            'level': 'DEBUG',                  # Show all log levels in development
            'formatter': 'verbose',            # Use detailed log format
        },
    },
    
    # Log message formatters - how log messages are structured
    'formatters': {
        'verbose': {
            # Comprehensive format including timestamp, level, module, process info
            'format': '%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    
    # Root logger configuration - applies to all Django logging
    'root': {
        'handlers': ['console'],  # Send all logs to console
        'level': 'DEBUG',         # Show debug level and above
    },
}

# ======================================================================
# DEVELOPMENT-SPECIFIC SETTINGS NOTES
# ======================================================================

# PERFORMANCE CONSIDERATIONS:
# - DEBUG=True disables template caching for immediate template changes
# - Static files are served by Django (not recommended for production)
# - Database queries are logged and can be inspected
# - Error pages include full request/response data

# SECURITY CONSIDERATIONS:
# - Debug mode exposes sensitive information in error pages
# - Secret key should still be secure even in development
# - CSRF protection is enabled but configured for local development
# - Admin URL can be customized to avoid /admin/ discovery

# WORKFLOW INTEGRATION:
# - Logging outputs to console for immediate feedback
# - Email testing through Mailpit web interface (localhost:8025)
# - Database accessible via localhost:5432 for external tools
# - API documentation available at localhost:8080/swagger

# ENVIRONMENT VARIABLE REQUIREMENTS:
# Create .envs/.env.local with these minimum variables:
# - DJANGO_SECRET_KEY=your-development-secret-key
# - DJANGO_ADMIN_URL=supersecret/
# - POSTGRES_DB=estate_db
# - POSTGRES_USER=estate_user
# - POSTGRES_PASSWORD=estate_password
# - POSTGRES_HOST=postgres
# - POSTGRES_PORT=5432
# - EMAIL_HOST=mailpit
# - EMAIL_PORT=1025
# - DEFAULT_FROM_EMAIL=noreply@localhost
# - DOMAIN=localhost:8080
# - SITE_NAME=Estate Development
# ======================================================================