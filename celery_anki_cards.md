# Celery Docker Setup - Anki Cards

## Card 1: Basic Celery Structure
**Front:** What are the three main Celery services in a Django project?
**Back:** 
- **Worker**: Executes the actual tasks
- **Beat**: Scheduler that sends tasks to workers at specified times  
- **Flower**: Web-based monitoring tool for Celery tasks and workers

## Card 2: Watchfiles Purpose
**Front:** What is the purpose of `watchfiles` in Celery development scripts?
**Back:** 
`watchfiles` monitors Python files for changes and automatically restarts Celery processes when changes are detected. It's only used in development - never in production. For production, use systemd or supervisor instead.

## Card 3: Celery Worker Command
**Front:** What is the basic command structure to start a Celery worker?
**Back:** 
```bash
celery.__main__.main --args '-A config.celery_app worker --loglevel=info'
```
- `-A config.celery_app`: Specifies the Celery application
- `worker`: Tells Celery to run in worker mode
- `--loglevel=info`: Sets logging level for informational messages

## Card 4: Celery Beat Command  
**Front:** What is the basic command structure to start Celery Beat (scheduler)?
**Back:**
```bash
celery.__main__.main --args '-A config.celery_app beat --loglevel=info'
```
- `beat`: Tells Celery to run in scheduler mode
- Must remove `celerybeat.pid` file before starting: `rm -f './celerybeat.pid'`

## Card 5: Flower Authentication
**Front:** How do you set up basic authentication for Celery Flower?
**Back:**
```bash
flower --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
```
- Uses environment variables for username and password
- Provides web UI at localhost:5555
- Example: admin:Pass123456

## Card 6: Celery Broker Configuration
**Front:** How do you specify the broker URL for Celery services?
**Back:**
```bash
-b "${CELERY_BROKER_URL}"
```
- The broker mediates communication between workers and clients
- In this project: Redis at `redis://redis:6379/0`
- Essential for task distribution and result storage

## Card 7: Docker Container Rebuild
**Front:** When do you need to rebuild Docker containers for Celery changes?
**Back:**
When you:
- Add new packages to requirements
- Add new services to docker-compose
- Add environment variables
- Change configuration files

Use: `make build` then `make up`

## Card 8: Bash Script Safety Options
**Front:** What do `set -o errexit` and `set -o nounset` do in bash scripts?
**Back:**
- `set -o errexit`: Exit immediately if any command fails (non-zero exit status)
- `set -o nounset`: Exit if trying to use undefined variables
- These make scripts fail fast and prevent silent errors

## Card 9: Watchfiles Filter
**Front:** Why use `--filter python` with watchfiles?
**Back:**
- Only monitors Python files for changes
- Prevents unnecessary restarts when non-Python files change (CSS, JS, etc.)
- Improves development efficiency by reducing false triggers

## Card 10: Production vs Development
**Front:** What's the key difference between Celery setup in development vs production?
**Back:**
- **Development**: Use `watchfiles` for auto-restart on code changes
- **Production**: Use process managers like systemd or supervisor
- Production needs stable, well-tested code that doesn't change frequently
- No auto-restart needed in production

## Card 11: Celery Entry Point
**Front:** What is `celery.__main__.main` in the start scripts?
**Back:**
- The main entry point of the Celery command-line tool
- Uses Python's double underscore (`__main__`) module convention
- Equivalent to running `celery` command directly
- Used with watchfiles to enable auto-restart functionality

## Card 12: File Structure Organization
**Front:** How should Celery start scripts be organized in a Django Docker project?
**Back:**
```
docker/local/django/celery/
├── beat/start.sh
├── worker/start.sh
└── flower/start.sh
```
Each service gets its own folder with a dedicated start script for clean separation of concerns.
