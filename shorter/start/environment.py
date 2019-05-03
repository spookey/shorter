from os import getenv, path
from string import ascii_letters, digits

APP_NAME = 'shorter'
MDL_NAME = __name__.split('.')[0]

THIS_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.abspath(path.dirname(THIS_DIR))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

MIGR_DIR = path.abspath(path.join(ROOT_DIR, 'migrate'))

LOG_BASE = getenv('LOG_BASE', path.abspath(path.join(ROOT_DIR, 'logs')))
LOG_FILE = getenv('LOG_FILE', '{}.log'.format(APP_NAME))
LOG_LVL = getenv('LOG_LVL', 'info')

DATABASE = getenv('DATABASE', 'sqlite://')
DATABASE_DEV = getenv('DATABASE_DEV', 'sqlite:///{}'.format(
    path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))
))

SECRET_FILE = getenv('SECRET_FILE', 'secret.key')
SECRET_BASE = getenv('SECRET_BASE', ROOT_DIR)

THEME = getenv('THEME', 'plain')
TITLE = getenv('TITLE', APP_NAME)
HTML_LANG = getenv('HTML_LANG', 'en')

SYM_POOL = ''.join((ascii_letters, digits))
SYM_MINI = 3

ERROR_CODES = (
    400, 401, 403, 404, 418,
    500, 501, 502, 503, 504,
)

CRAWLERS = (
    'aol',
    'applebot',
    'ask',
    'baidu',
    'baiduspider',
    'bing',
    'bingbot',
    'duckduckbot',
    'embedly',
    'facebook',
    'google',
    'googlebot',
    'twitterbot',
    'yahoo',
    'yandex',
    'yandexbot',
)
