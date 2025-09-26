#! /bin/bash

set -o errexit

set -o nounset

exec watchfiles --filter python celery.__main__.main \
 --args \
 "-A config.celery_app -b \"${CELERY_BROKER_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""

# flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\"" This command starts the celery flower monitoring
# tool, which provides a web based user interface for monitoring and managing celery tasks and workers.
# And so here we are seeing the basic auth is going to be the celery flower user and the celery flower password.
# This is just going to enable basic authentication for the flower web interface.
# The username and password are going to be sent using the celery flower user and the celery flower password environment variables.

# -b \"${CELERY_BROKER_URL}\" specifies the broker URL for celery to connect to.
# The broker is responsible for mediating communication between the celery workers and the clients that submit tasks.
# The CELERY_BROKER_URL environment variable is expected to contain the URL of the message broker that celery should use.
# This is Redis. CELERY_BROKER_URL="redis://redis:6379/0" as defined in the .env.local file.
# The broker URL is specified using the -b option, which is a shorthand for --broker.
# This tells celery to use the specified broker for sending and receiving messages related to task execution

# The watchfiles tool is used to monitor changes in Python files and automatically restart the celery flower process when changes are detected.
# This is particularly useful during development, as it allows developers to see the effects of their code changes in real time without having to manually restart the celery flower process.
# The --filter python option ensures that only changes to Python files trigger a restart.
# The --args option is used to pass arguments to the celery flower command.
# The exec command is used to replace the current shell process with the watchfiles process.
# This ensures that the watchfiles process becomes the main process of the container.
# This is important for proper signal handling and process management within the Docker container.
# Overall, this script sets up a development environment for monitoring celery tasks using flower,
# with automatic restarts on code changes, making it easier to develop and debug celery tasks.  


# When dealing with Docker, always remember that packages are installed in our containers at build time and not runtime.

