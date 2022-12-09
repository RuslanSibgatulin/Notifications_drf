# Notifications - сервис уведомлений.

Сервис управления рассылками, API администрирования и получения статистики. Метод отправки сообщений - сторонний СМС сервис.


## Используемые технологии
- Код приложения на Python
- Фреймворк [Django 4.1](https://docs.djangoproject.com/en/4.1/) + [DRF](https://www.django-rest-framework.org/#installation)
- Очередь задач [Celery](https://docs.celeryq.dev/en/stable/#) + Redis
- СУБД - Postgres
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Клонировать репозиторий
    git@github.com:RuslanSibgatulin/Notifications_drf.git

## Переменные окружения
Подготовить файлы с переменными окружения по аналогии с файлами `docker/envs/*.example` и пересохранить в файлы `*.env`

## Запуск

    make start
    make init

# Функциональность
- [Админ-панель](http://127.0.0.1/admin/)
- [OpenAPI документация](http://127.0.0.1/apidocs/)
