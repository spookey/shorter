from os import path

from shorter.environment import BASE_DIR, MIGR_DIR, ROOT_DIR

SELF_DIR = path.abspath(path.dirname(__file__))


def test_rootdir():
    assert ROOT_DIR == path.dirname(SELF_DIR)


def test_basedir():
    assert BASE_DIR == path.join(path.dirname(SELF_DIR), 'shorter')


def test_migratedir():
    assert MIGR_DIR == path.join(path.dirname(SELF_DIR), 'migrate')
