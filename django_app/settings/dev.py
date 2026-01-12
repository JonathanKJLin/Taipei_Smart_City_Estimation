"""
Development Settings
開發環境專用設定
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Development-specific apps
INSTALLED_APPS += [
    'django_extensions',  # Optional: for shell_plus, etc.
]

# Database for development (SQLite as fallback)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Disable HTTPS redirect in development
SECURE_SSL_REDIRECT = False

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
