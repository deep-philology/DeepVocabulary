import os

from django.urls import reverse_lazy

import dj_database_url


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

DEBUG = bool(int(os.environ.get("DEBUG", "1")))

DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost/deep-vocabulary")
}

ALLOWED_HOSTS = [
    "localhost",
    "vocab.perseus.org",
    "vocab-dev.perseus.org",
    ".herokuapp.com"
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "$if_w1$7hxi@3yb@&g!--v!pvbw$w)+s)ic-!haufho%_wqz$w"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "deep_vocabulary.context_processors.settings"
            ],
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.RefreshIDToken",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "querycount.middleware.QueryCountMiddleware",
]

ROOT_URLCONF = "deep_vocabulary.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "deep_vocabulary.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    # templates
    "bootstrapform",
    "pinax.templates",

    # external
    "account",
    "mozilla_django_oidc",
    "pinax.eventlog",
    "pinax.webanalytics",
    "raven.contrib.django.raven_compat",
    "corsheaders",
    "letsencrypt",

    # project
    "deep_vocabulary",
]

ADMIN_URL = "admin:index"
CONTACT_EMAIL = "support@example.com"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format": "{asctime} {name:<12} {levelname:<8} {message}",
            "style": "{",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "{asctime} {name:<12} {levelname:<8} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["require_debug_true"],
            "level": "DEBUG",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
    "deep_vocabulary.auth.PinaxOIDCAuthenticationBackend",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = bool(int(os.environ.get("SECURE_SSL_REDIRECT", "0")))
SECURE_REDIRECT_EXEMPT = [
    r"\.well-known/acme-challenge/.+",
]

if "SENTRY_DSN" in os.environ:
    RAVEN_CONFIG = {
        "dsn": os.environ["SENTRY_DSN"],
    }

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^.*/json/$"

SCAIFE_HOST = os.environ.get("SCAIFE_HOST", "https://scaife.perseus.org")

OIDC_HOST = os.environ.get("OIDC_HOST", "http://localhost:3000")
OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_RP_CLIENT_SECRET")
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_HOST}/openid/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_HOST}/openid/token"
OIDC_OP_USER_ENDPOINT = f"{OIDC_HOST}/openid/userinfo"
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 15
OIDC_RP_SCOPES = "openid email profile"

# reverse_lazy is required because mozilla-django-oidc does not handle
# URLconf names
LOGIN_REDIRECT_URL = reverse_lazy(ACCOUNT_LOGIN_REDIRECT_URL)
LOGIN_REDIRECT_URL_FAILURE = reverse_lazy("account_login_failure")
LOGOUT_REDIRECT_URL = reverse_lazy(ACCOUNT_LOGOUT_REDIRECT_URL)

USE_X_FORWARDED_HOST = True
