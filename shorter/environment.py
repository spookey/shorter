from os import getenv, path

BASE_DIR = path.abspath(path.dirname(__file__))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

MIGR_DIR = path.abspath(path.join(ROOT_DIR, 'migrate'))


DATABASE = getenv('DATABASE', 'sqlite://')
DATABASE_DEV = getenv('DATABASE_DEV', 'sqlite:///{}'.format(
    path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))
))

SECRET_FILE = getenv('SECRET_FILE', 'secret.key')
SECRET_BASE = getenv('SECRET_BASE', ROOT_DIR)
