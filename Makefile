build:
	docker compose -f local.yml up --build -d --remove-orphans api postgres mailpit client redis celeryworker celerybeat flower nginx

up: 
	docker compose -f local.yml up -d api postgres mailpit client redis celeryworker celerybeat flower nginx

stop-pg:
	sudo systemctl stop postgresql
	# optionally disable the service so it doesn't start on boot
	sudo systemctl disable postgresql

down:
	docker compose -f local.yml down postgres mailpit client redis celeryworker celerybeat flower nginx

down-v:
	docker compose -f local.yml down -v postgres mailpit client redis celeryworker celerybeat flower nginx

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs api

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

showmigrations:
	docker compose -f local.yml run --rm api python manage.py showmigrations
	
collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --noinput --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

db-volume:
	docker volume inspect django_real_estate_estate_prod_postgres_data

mailpit-volume:
	docker volume inspect django_real_estate_estate_mailpit_data

estate-db:
	docker compose -f local.yml exec postgres psql --username=bernard --dbname=estate