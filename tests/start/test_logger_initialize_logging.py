from logging import DEBUG, INFO, NOTSET, getLogger

from shorter.start.environment import MDL_NAME
from shorter.start.logger import FORMATTER, ROTATE, STREAM, initialize_logging


def test_formatter_preinit():
    assert STREAM.formatter is None
    assert ROTATE.formatter is None


def test_init_basic():
    log = getLogger(MDL_NAME)
    assert log.name == MDL_NAME

    assert log.level == NOTSET
    assert not log.handlers

    initialize_logging()

    assert log.level == INFO
    assert STREAM in log.handlers
    assert ROTATE in log.handlers
    assert len(log.handlers) == 2


def test_init_level_fallback():
    log = getLogger(MDL_NAME)

    initialize_logging('❌')

    assert log.level == DEBUG


def test_formatter_postinit():
    assert STREAM.formatter == FORMATTER
    assert ROTATE.formatter == FORMATTER
