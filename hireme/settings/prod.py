from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")  # noqa: F405
    if host.strip()
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "hireme"),  # noqa: F405
        "USER": os.getenv("POSTGRES_USER", "hireme"),  # noqa: F405
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),  # noqa: F405
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),  # noqa: F405
        "PORT": os.getenv("POSTGRES_PORT", "5432"),  # noqa: F405
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"  # noqa: F405
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True").lower() == "true"  # noqa: F405
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True").lower() == "true"  # noqa: F405
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600"))  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
