import os
import logging
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger("django")
load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "news.apps.NewsConfig",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django_filters",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_apscheduler",
    "rest_framework",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "NewsPaper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "NewsPaper.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_FORMS = {"signup": "news.forms.CommonSignupForm"}

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/news/profile/"
LOGOUT_REDIRECT_URL = "/news/"

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True
SITE_URL = "http://127.0.0.1:8000"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("ru", "Русский"),
    ("en-us", "English"),
]

TIME_ZONE = "UTC"

USE_I18N = True

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [BASE_DIR / "static"]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache_files",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "style": "{",
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%d.%m.%Y %H-%M-%S",
        },
        "simple_warning": {
            "format": "%(asctime)s %(levelname)s %(message)s %(pathname)s"
        },
        "simple_error": {
            "format": "%(asctime)s %(levelname)s %(message)s %(exc_info)s"
        },
        "general": {
            "format": "%(asctime)s %(levelname)s %(module)s %(message)s",
            "datefmt": "%d.%m.%Y %H-%M-%S",
        },
        "errors": {
            "format": "%(asctime)s %(levelname)s %(pathname)s %(message)s %(exc_info)s",
            "datefmt": "%d.%m.%Y %H-%M-%S",
        },
        "email": {
            "format": "%(asctime)s %(levelname)s %(message)s %(pathname)s",
            "datefmt": "%d.%m.%Y %H-%M-%S",
        },
        "security": {
            "format": "%(asctime)s %(levelname)s %(module)s %(message)s",
            "datefmt": "%d.%m.%Y %H-%M-%S",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console_warning": {
            "level": "WARNING",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple_warning",
        },
        "console_error": {
            "level": "ERROR",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple_error",
        },
        "general": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "filename": "logs/general.log",
            "formatter": "general",
        },
        "errors": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "logs/errors.log",
            "formatter": "errors",
        },
        "security": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/security.log",
            "formatter": "security",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "email",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "console_warning", "console_error", "general"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["errors", "mail_admins"],
            "propagate": True,
        },
        "django.server": {
            "handlers": ["errors", "mail_admins"],
            "propagate": True,
        },
        "django.template": {
            "handlers": ["errors"],
            "propagate": True,
        },
        "django.db_backends": {
            "handlers": ["errors"],
            "propagate": True,
        },
        "django.security": {
            "handlers": ["security"],
            "propagate": True,
        },
    },
}
