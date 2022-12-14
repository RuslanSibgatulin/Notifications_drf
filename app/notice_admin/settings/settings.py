import os
from pathlib import Path

from celery.schedules import crontab
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "notice",
    "rest_framework",
    "drf_yasg",
    "phonenumber_field"
]

ROOT_URLCONF = "notice_admin.urls"

WSGI_APPLICATION = "notice_admin.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "notice_database"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
        "OPTIONS": {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            "options": "-c search_path=public,content"
        },
    }
}

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.joinpath("static")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_SCHEDULE_INTERVAL = int(os.environ.get("CELERY_SCHEDULE_INTERVAL", 1))
CELERY_BEAT_SCHEDULE = {
    "send_notices": {
        "task": "notice.tasks.send_notices",
        "schedule": crontab(minute=f"*/{CELERY_SCHEDULE_INTERVAL}"),
    },
}

include(
    "logger.py",  # LOGGING
    "middleware.py",  # Middleware
    "templates.py",  # Templates
    "components/auth.py",  # Auth
)
