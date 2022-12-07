## ----------------------------------------------------------------------
## Makefile is to manage Notice Admin.
## ----------------------------------------------------------------------
include docker/envs/NoticeAdmin.env
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
