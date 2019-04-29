from os import getenv, path

APP_NAME = 'shrtr'
MDL_NAME = __name__.split('.')[0]

THIS_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.abspath(path.dirname(THIS_DIR))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

MIGR_DIR = path.abspath(path.join(ROOT_DIR, 'migrate'))

LOGS_DIR = getenv('LOGS_DIR', path.abspath(path.join(ROOT_DIR, 'logs')))
LOGS_LVL = getenv('LOGS_LVL', 'info')

DATABASE = getenv('DATABASE', 'sqlite://')
DATABASE_DEV = getenv('DATABASE_DEV', 'sqlite:///{}'.format(
    path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))
))

SECRET_FILE = getenv('SECRET_FILE', 'secret.key')
SECRET_BASE = getenv('SECRET_BASE', ROOT_DIR)

THEME = getenv('THEME', 'default')


ERROR_CODES = (
    400, 401, 403, 404, 418,
    500, 501, 502, 503, 504,
)
