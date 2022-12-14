## ----------------------------------------------------------------------
## Makefile is to manage Notice Admin.
## ----------------------------------------------------------------------
include docker/envs/NoticeAdmin-dev.env
export

compose_files=-f docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Start project
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files) up -d --build --force-recreate

stop:
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files) down

init:  ## First and full initialization. Create database, superuser and collect static files
		docker exec -it notice_django bash -c \
		'python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py collectstatic --noinput'

runserver:
		cd app && python manage.py runserver

shell:
		cd app && python manage.py shell

worker-celery:
		cd app && celery -A notice_admin worker --loglevel=INFO

ci-tests:
		cd app && python manage.py test --settings=notice_admin.settings.settings_local

lint-install:
		pip install lxml mypy wemake-python-styleguide flake8-html types-requests types-pytz

lint:
		isort app/
		flake8 app/ --show-source
		mypy app/ --ignore-missing-imports --no-strict-optional --exclude /migrations/ --exclude /tests/
