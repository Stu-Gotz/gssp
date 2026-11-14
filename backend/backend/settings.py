import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

PRODUCTION = os.environ.get("NODE_ENV") == "production"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key")
DEBUG = not PRODUCTION

# ------------------------------------
# CHANGE IN PRODUCTION
# ====================================
ALLOWED_HOSTS = ["*"]

""
INSTALLED_APPS = [
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

# ------------------------------------
# Postgres
# ====================================
if PRODUCTION:
    DATABASES = {
        "default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("LOCAL_DATABASE"),
            "USER": os.environ.get("LOCAL_USER"),
            "PASSWORD": os.environ.get("LOCAL_PASS"),
            "HOST": os.environ.get("LOCAL_HOST", "localhost"),
            "PORT": os.environ.get("LOCAL_PORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }

# ------------------------------------
# Etc
# ====================================
JWT_SECRET = os.environ.get("JWT_SECRET", "secretkey")
CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = "static/"
WHITENOISE_ROOT = BASE_DIR.parent / "application" / "public"
WHITENOISE_INDEX_FILE = True

USE_TZ = True
TIME_ZONE = "UTC"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
