# apps/config/db.py
from environ import Env

env = Env()
Env.read_env() 

DB_BACKENDS = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DBNAME', default=''),
        'USER': env('DBUSER', default=''),
        'PASSWORD': env('DBPASSWORD', default=''),
        'HOST': env('DBHOST', default=''),
        'PORT': env('DBPORT', default=''),
    }
}


def get_database_config():
    # Choose backend key from environment variable, default sqlite for tests
    backend = 'sqlite' if env.bool('USE_SQLITE', default=True) else 'postgres'
    return {'default': DB_BACKENDS[backend]}
