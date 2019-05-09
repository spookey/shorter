from logging import DEBUG, INFO, getLogger

from shorter.start.environment import MDL_NAME
from shorter.start.logger import FORMATTER, STREAM, initialize_logging


def test_init_basic():
    log = getLogger(MDL_NAME)
    assert log.name == MDL_NAME

    initialize_logging('info')

    assert log.level == INFO


def test_init_level_fallback():
    log = getLogger(MDL_NAME)

    initialize_logging('❌')

    assert log.level == DEBUG


def test_formatter():
    assert STREAM.formatter == FORMATTER
