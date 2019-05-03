from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, StreamHandler, getLogger
)
from logging.handlers import RotatingFileHandler
from os import path

from shorter.start.environment import LOG_BASE, LOG_FILE, LOG_LVL, MDL_NAME

MAX_BYTES = 10 * (1024 * 1024)
LOG_COUNT = 9

FORMATTER = Formatter('''
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [%(pathname)s:%(lineno)d]
  %(message)s
'''.lstrip())

STREAM = StreamHandler(stream=None)
ROTATE = RotatingFileHandler(
    path.abspath(path.join(LOG_BASE, LOG_FILE)),
    maxBytes=MAX_BYTES,
    backupCount=LOG_COUNT
)

LOG_LEVELS = {
    'debug': DEBUG,
    'error': ERROR,
    'info': INFO,
    'warn': WARNING,
    'warning': WARNING,
}


def initialize_logging(level_name=LOG_LVL):
    logger = getLogger(MDL_NAME)
    level = LOG_LEVELS.get(level_name, DEBUG)

    logger.setLevel(level)

    STREAM.setLevel(level)
    STREAM.setFormatter(FORMATTER)
    logger.addHandler(STREAM)

    ROTATE.setLevel(level)
    ROTATE.setFormatter(FORMATTER)
    logger.addHandler(ROTATE)
