#!/bin/bash

set -o errexit

set -o nounset

# Execute watch files.Run the watch files program to monitor only Python files for changes
# and automatically restart the specified command when changes are detected. -filter python.
# Watch files will restart the celery worker every time a change is detected (used only for development).
# For production use systemd or supervisord to manage the celery worker process.
# celery.__main__.main --args
# This is the main entry point of the celery command line tool.
# -A config.celery_app worker command is the config celery_app we had created before in the config folder.
# Then the worker argument tells celery to run in the worker mode.
# --loglevel=info option sets the log level to info, which means that informational messages, warnings and errors will be logged.

exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker --loglevel=info' 
