from os import path

from shorter.start.environment import (
    BASE_DIR, LOGS_DIR, MIGR_DIR, ROOT_DIR, THIS_DIR
)

TEST_DIR = path.abspath(path.dirname(path.dirname(__file__)))


def test_rootdir():
    assert ROOT_DIR == path.dirname(TEST_DIR)


def test_basedir():
    assert BASE_DIR == path.join(path.dirname(TEST_DIR), 'shorter')


def test_thisdir():
    assert THIS_DIR == path.join(path.dirname(TEST_DIR), 'shorter', 'start')


def test_migratedir():
    assert MIGR_DIR == path.join(path.dirname(TEST_DIR), 'migrate')


def test_loggingdir():
    assert LOGS_DIR == path.join(path.dirname(TEST_DIR), 'logs')
