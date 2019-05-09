from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, StreamHandler, getLogger
)

from shorter.start.environment import LOG_LVL, MDL_NAME

FORMATTER = Formatter('''
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [%(pathname)s:%(lineno)d]
  %(message)s
'''.lstrip())

STREAM = StreamHandler(stream=None)

LOG_LEVELS = {
    'debug': DEBUG,
    'error': ERROR,
    'info': INFO,
    'warn': WARNING,
    'warning': WARNING,
}


def initialize_logging(level_name=LOG_LVL):
    root_logger = getLogger()
    main_logger = getLogger(MDL_NAME)
    level = LOG_LEVELS.get(level_name, DEBUG)

    main_logger.setLevel(level)

    STREAM.setLevel(level)
    STREAM.setFormatter(FORMATTER)
    root_logger.addHandler(STREAM)
