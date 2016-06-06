from .base_settings import *


SECRET_KEY = 'o5n!*%81b3nc0+u#ln719abe@s9)($j$(w%$3*^1o=wu(36h1!'

ALLOWED_HOSTS = [
    "localhost",
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# litel mydb
