#!/bin/bash

# ==============================================================================
# Django Real Estate - Docker Entrypoint Script
# ==============================================================================
# This script serves as the entrypoint for the Django container. It handles
# database connectivity waiting and proper process management.
#
# Purpose:
# 1. Wait for PostgreSQL database to be available before starting Django
# 2. Provide proper signal handling and process management
# 3. Execute the actual application command (passed as arguments)
#
# Usage:
#   This script is automatically called by Docker when the container starts.
#   It receives the command to execute (e.g., "/start") as arguments ($@).
#
# Environment Variables Required:
#   POSTGRES_DB       - Database name
#   POSTGRES_USER     - Database username  
#   POSTGRES_PASSWORD - Database password
#   POSTGRES_HOST     - Database host (usually "postgres" in compose)
#   POSTGRES_PORT     - Database port (usually "5432")
#
# Flow:
#   Container Start → Entrypoint → Wait for DB → Execute Command → Django Runs
# ==============================================================================

# Exit immediately if any command fails (prevents silent failures)
set -o errexit

# Exit if any command in a pipeline fails (not just the last one)
set -o pipefail

# Exit if any undefined variable is used (catches typos in variable names)
set -o nounset

# ==============================================================================
# DATABASE CONNECTIVITY WAITING
# ==============================================================================
# This section implements a robust database waiting mechanism using Python.
# We use Python instead of shell tools because:
# 1. psycopg2 gives accurate PostgreSQL-specific connection testing
# 2. More reliable than simple port checking (port open ≠ database ready)
# 3. Provides detailed error information for debugging

python << END 
import sys
import time
import psycopg2

# Configuration for database waiting
suggest_unrecoverable_after = 30  # Seconds before suggesting there might be an issue
start = time.time()

# Infinite loop until database connection succeeds
while True:
    try:
        # Attempt to connect to PostgreSQL using environment variables
        # These variables are injected by Docker Compose from .env.local
        psycopg2.connect(
            dbname="${POSTGRES_DB}",      # Database name (e.g., "estate")
            user="${POSTGRES_USER}",      # Database user (e.g., "bernard")
            password="${POSTGRES_PASSWORD}", # Database password
            host="${POSTGRES_HOST}",      # Database host (e.g., "postgres")
            port="${POSTGRES_PORT}",      # Database port (e.g., "5432")
        )
        # If we reach here, connection succeeded - break out of loop
        break
    except psycopg2.OperationalError as error:
        # Database not ready yet - this is expected during startup
        sys.stderr.write("Waiting for Postgres to be available...\n")
        
        # If waiting too long, provide diagnostic information
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write(
                " This is taking longer than expected. "
                "The following exception may be indicative of an unrecoverable error: '{}'\n".format(error)
            )
        
        # Wait 1 second before trying again
        time.sleep(1)
END

# Database is now available - log success message to stderr
# Using >&2 sends this to stderr instead of stdout, keeping logs clean
>&2 echo "PostgreSQL is available"

# ==============================================================================
# COMMAND EXECUTION
# ==============================================================================
# Execute the command passed to this script (e.g., "/start")
# 
# exec vs regular command execution:
# - exec: Replaces the current process (entrypoint) with the new command
# - regular: Runs command as child process, keeping entrypoint running
#
# Why use exec:
# 1. Clean process tree - no unnecessary parent process
# 2. Proper signal handling - Docker signals go directly to Django
# 3. Correct exit codes - Django's exit code becomes container's exit code
# 4. Memory efficiency - one less process in memory
#
# "$@" explanation:
# - $@ contains all arguments passed to this script
# - In quotes, it preserves each argument as separate words
# - Example: if called with "/start --reload", $@ becomes ["/start", "--reload"]
exec "$@"