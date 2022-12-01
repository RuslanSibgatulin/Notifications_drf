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

runserver:
		python app/manage.py runserver

migrate:  ## Apply database changes
		python app/manage.py makemigrations
		python app/manage.py migrate

su:
		python app/manage.py createsuperuser
