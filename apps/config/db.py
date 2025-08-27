# apps/config/db.py
from environ import Env
from pathlib import Path

env = Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # adjust if needed
env_file = BASE_DIR / ".env"
env.read_env(env_file)

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
    backend = 'sqlite' if env.bool('USE_SQLITE', default=False) else 'postgres'
    return {'default': DB_BACKENDS[backend]}
