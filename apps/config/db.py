# apps/config/db.py
from environ import Env

env = Env()

DB_BACKENDS = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DBNAME'),
        'USER': env('DBUSER'),
        'PASSWORD': env('DBPASSWORD'),
        'HOST': env('DBHOST'),
        'PORT': env('DBPORT'),
    }
}


def get_database_config():
    # Choose backend key from environment variable, default sqlite for tests
    backend = 'sqlite' if env.bool('USE_SQLITE', default=False) else 'postgres'
    return {'default': DB_BACKENDS[backend]}
