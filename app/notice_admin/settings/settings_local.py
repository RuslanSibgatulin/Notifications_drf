import os
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", False) == "True"

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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "notice_database.sqlite",
        "TEST": {
            "NAME": BASE_DIR / "test_notice_database.sqlite",
        }
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

include(
    "logger.py",  # LOGGING
    "middleware.py",  # Middleware
    "templates.py",  # Templates
    "auth.py",  # Auth
)
