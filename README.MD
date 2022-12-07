# Сервис Notifications - уведомления.

Сервис управления рассылками API администрирования и получения статистики.
ТЗ проекта https://www.craft.do/s/n6OVYFVUpq0o6L


## Используемые технологии
- Код приложения на Python
- Фреймворк [Django 4.1](https://docs.djangoproject.com/en/4.1/) + [DRF](https://www.django-rest-framework.org/#installation)
- СУБД - Postgres
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
1. Клонировать репозиторий

2. Подготовить файлы с переменными окружения по аналогии с файлами `docker/envs/*.example` и пересохранить в файлы `*.env`

3. Выполнить команду

    make start

# Функциональность
- [Админ-панель](http://127.0.0.1/admin/). Логин `admin` пароль `admin`
- [OpenAPI документация](http://127.0.0.1/apidocs/)
