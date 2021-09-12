
up:
	docker-compose up

run:
	docker-compose up -d

build:
	docker-compose build

app:
	docker-compose exec django python manage.py startapp $(APP_NAME)
	
superuser:
	docker-compose exec django python manage.py createsuperuser

django:
	docker-compose -f docker-compose.yml restart django

migrate:
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate

statics:
	docker-compose exec django python manage.py collectstatic --no-input

makemessages:
	docker-compose exec django python manage.py makemessages -l es
	docker-compose exec django python manage.py makemessages -l en

compilemessages:
	docker-compose exec django python manage.py compilemessages -f

test:
	docker-compose exec django python manage.py test


prod-up:
	docker-compose -f docker-compose.prod.yml up

prod-run:
	docker-compose -f docker-compose.prod.yml up -d

prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-app:
	docker-compose -f docker-compose.prod.yml exec django python manage.py startapp $(APP_NAME)

prod-superuser:
	docker-compose -f docker-compose.prod.yml exec django python manage.py createsuperuser

prod-django:
	docker-compose -f docker-compose.prod.yml restart django

prod-migrate:
	docker-compose -f docker-compose.prod.yml exec django python manage.py makemigrations
	docker-compose -f docker-compose.prod.yml exec django python manage.py migrate

prod-statics:
	docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic --no-input

prod-makemessages:
	docker-compose -f docker-compose.prod.yml exec django python manage.py makemessages -l es
	 docker-compose -f docker-compose.prod.yml exec django python manage.py makemessages -l en

prod-compilemessages:
	docker-compose -f docker-compose.prod.yml exec django python manage.py compilemessages -f

prod-test:
	docker-compose -f docker-compose.prod.yml exec django python manage.py test


reset:
	docker-compose down -v
	rm -rf ./postgres-data

clean:
	rm -rf src/*/migrations/00**.py
	find . -name "*.pyc" -exec rm -- {} +
	rm -rf src/*/migrations/__pycache__/*