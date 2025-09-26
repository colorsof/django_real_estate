# ==============================================================================
# Django Real Estate - Local Development Dockerfile
# ==============================================================================
# This multi-stage Dockerfile builds a Django application container optimized 
# for local development. It uses two stages to separate dependency building 
# from the final runtime image, improving build efficiency and image size.
#
# Build arguments:
#   BUILD_ENVIRONMENT: Determines which requirements file to use (default: local)
#
# Usage:
#   docker build -f docker/local/django/Dockerfile -t estate_api .
#   docker run -p 8000:8000 estate_api
# ==============================================================================

# Base Python image - using slim variant for smaller size while keeping essential tools
FROM docker.io/python:3.11-slim as python

# ==============================================================================
# STAGE 1: DEPENDENCY BUILD STAGE
# ==============================================================================
# This stage compiles Python wheels for all dependencies. Wheels are pre-built
# packages that install faster and don't require compilation in the final image.
# This stage can be cached and reused across builds when requirements don't change.

FROM python AS python-build-stage

# Build argument to select environment-specific requirements file
# Options: local, production (corresponds to requirements/local.txt, requirements/production.txt)
ARG BUILD_ENVIRONMENT=local

# Install build tools needed for compiling Python packages with C extensions
# - build-essential: gcc, make, and other compilation tools
# - libpq-dev: PostgreSQL client library headers (needed for psycopg2)
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev 
    
# Copy requirements files to the container
# This copies the entire requirements/ directory structure
COPY ./requirements .

# Build wheels for all Python dependencies
# Wheels are faster to install and don't require compilation on target systems
# --wheel-dir: Directory to store the built wheels
# --no-deps: Don't install dependencies, just build wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt


# ==============================================================================
# STAGE 2: RUNTIME STAGE
# ==============================================================================
# This stage creates the final runtime image without build tools, keeping it lean.
# It installs the pre-built wheels from stage 1 and sets up the application environment.

FROM python as python-run-stage

# Build environment argument (same as stage 1)
ARG BUILD_ENVIRONMENT=local

# Application home directory inside the container
ARG APP_HOME=/app

# ==============================================================================
# PYTHON ENVIRONMENT CONFIGURATION
# ==============================================================================

# Prevent Python from writing .pyc files to disk
# These bytecode files aren't needed in containers and can slow down startup
ENV PYTHONDONTWRITEBYTECODE 1

# Force Python to run in unbuffered mode
# This ensures print statements and logs appear immediately in Docker logs
# Critical for real-time log monitoring and debugging
ENV PYTHONUNBUFFERED 1

# Store the build environment for runtime reference
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Set the working directory for all subsequent commands
WORKDIR ${APP_HOME}

# ==============================================================================
# SYSTEM DEPENDENCIES AND DEVELOPMENT TOOLS
# ==============================================================================

# Install development and debugging tools for local development
# - sudo: Administrative privileges for debugging
# - git: Version control (useful for development workflows)
# - bash-completion: Tab completion for better developer experience
# - nano: Simple text editor for quick file edits
# - ssh: SSH client for remote operations
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh

# ==============================================================================
# USER AND DIRECTORY SETUP
# ==============================================================================

# Create a dedicated user for running Django (security best practice)
# Running as root inside containers is a security risk
# --system: Create a system user (not a regular user account)
# --ingroup: Add user to the django group
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

# ==============================================================================
# RUNTIME DEPENDENCIES
# ==============================================================================

# Install runtime libraries needed by the application
# - libpq-dev: PostgreSQL client library (needed by psycopg2 at runtime)
# - gettext: Internationalization tools for Django's translation system
# Clean up package cache to reduce image size
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    &&rm -rf /var/lib/apt/lists/*

# ==============================================================================
# PYTHON PACKAGE INSTALLATION
# ==============================================================================

# Copy pre-built wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels

# Install all Python packages from the wheels
# --no-cache-dir: Don't cache downloaded packages (saves space)
# --no-index: Don't use PyPI, only use local wheels
# --find-links: Look for packages in the wheels directory
# Remove wheels after installation to save space
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# ==============================================================================
# SCRIPT SETUP
# ==============================================================================

# Copy and prepare the entrypoint script
# The entrypoint handles database connectivity waiting and signal handling
# --chown: Set file ownership to django user
COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint

# Remove Windows line endings (CRLF -> LF) for cross-platform compatibility
# This prevents "command not found" errors on Linux when scripts are edited on Windows
RUN sed -i 's/\r$//g' /entrypoint

# Make the entrypoint script executable
RUN chmod +x /entrypoint

# Copy and prepare the start script
# The start script runs migrations, collects static files, and starts the Django server
COPY --chown=django:django ./docker/local/django/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=django:django ./docker/local/django/celery/worker/start.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY --chown=django:django ./docker/local/django/celery/beat/start.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY --chown=django:django ./docker/local/django/celery/flower/start.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# ==============================================================================
# APPLICATION CODE
# ==============================================================================

# Copy the entire Django application code to the container
# This includes: manage.py, config/, core_apps/, requirements/, etc.
# --chown: Ensure all files are owned by the django user
COPY --chown=django:django . ${APP_HOME}

# Ensure the django user owns the application directory
# This is necessary for Django to write logs, create files, etc.
RUN chown django:django ${APP_HOME} 

# ==============================================================================
# SECURITY AND RUNTIME CONFIGURATION
# ==============================================================================

# Switch to the non-root django user for security
# All subsequent commands and the final container process run as this user
USER django

# Set the entrypoint script as the container's entrypoint
# The entrypoint runs first and handles:
# 1. Waiting for database connectivity
# 2. Executing the command passed from docker-compose (usually /start)
# 3. Proper signal handling for graceful shutdowns
ENTRYPOINT ["/entrypoint"]

# ==============================================================================
# CONTAINER STARTUP FLOW
# ==============================================================================
# When this container starts:
# 1. ENTRYPOINT runs /entrypoint script
# 2. Entrypoint waits for PostgreSQL to be available
# 3. Entrypoint executes the command from docker-compose.yml (/start)
# 4. Start script runs: migrate -> collectstatic -> runserver
# 5. Django development server starts on 0.0.0.0:8000
#
# The command is specified in docker-compose.yml:
#   command: /start
# ==============================================================================