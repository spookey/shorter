from os import getenv, path
from string import ascii_letters, digits

from shorter.start.helper import parse_bool, parse_int

APP_NAME = "shorter"
MDL_NAME = __name__.split(".", maxsplit=1)[0]

THIS_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.abspath(path.dirname(THIS_DIR))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

LOG_LVL = getenv("LOG_LVL", "info")

DATABASE = getenv("DATABASE", "sqlite://")
DATABASE_DEV = getenv(
    "DATABASE_DEV",
    f"sqlite:///{path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))}",
)

SECRET_FILE = getenv("SECRET_FILE", "secret.key")
SECRET_BASE = getenv("SECRET_BASE", ROOT_DIR)

BLOCK_FILE = getenv("BLOCK_FILE", "blocklist.txt")
BLOCK_BASE = getenv("BLOCK_BASE", ROOT_DIR)

CSRF_STRICT = parse_bool(getenv("CSRF_STRICT", "true"), fallback=True)

THEME = getenv("THEME", "default")
TITLE = getenv("TITLE", APP_NAME)
HTML_LANG = getenv("HTML_LANG", "en")

DELAY_MIN = parse_int(getenv("DELAY_MIN", "0"), fallback=0)
DELAY_MAX = parse_int(getenv("DELAY_MAX", "30"), fallback=30)
DELAY_DEF = parse_int(getenv("DELAY_DEF", "6"), fallback=6)
DELAY_STP = parse_int(getenv("DELAY_STP", "3"), fallback=3)

SYM_POOL = "".join((ascii_letters, digits))
SYM_MINI = parse_int(getenv("SYM_MINI", "3"), fallback=3)

PAGINATION = parse_int(getenv("PAGINATION", "100"), fallback=100)

RX_XSS_STORED = r".+\'\+.+//"

ERROR_CODES = (
    400,
    401,
    403,
    404,
    418,
    #
    500,
    501,
    502,
    503,
    504,
)

CRAWLERS = (
    "aol",
    "applebot",
    "ask",
    "baiduspider",
    "bing",
    "bingbot",
    "duckduckbot",
    "embedly",
    "google",
    "googlebot",
    "yahoo",
    "yandexbot",
)
SOCIAL = (
    "facebookexternalhit",
    "facebot",
    "twitterbot",
)
