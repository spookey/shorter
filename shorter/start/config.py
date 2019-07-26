from os import path, urandom
from re import IGNORECASE
from re import compile as rx_compile

from shorter.start.environment import (
    APP_NAME, BLOCK_BASE, BLOCK_FILE, CSRF_STRICT, DATABASE, DATABASE_DEV,
    HTML_LANG, PAGINATION, ROOT_DIR, SECRET_BASE, SECRET_FILE, THEME, TITLE
)


def secret_key(base=SECRET_BASE, filename=SECRET_FILE):
    location = path.abspath(path.join(base, filename))
    if not path.exists(location):
        secret = urandom(512)
        with open(location, 'wb') as handle:
            handle.write(secret)
        return secret
    with open(location, 'rb') as handle:
        return handle.read()


def theme_folders(root=ROOT_DIR, theme=THEME):
    base = path.abspath(path.join(root, 'themes', theme))
    stat = path.join(base, 'static')
    tmpl = path.join(base, 'templates')
    if not all(path.exists(pth) for pth in (stat, tmpl)):
        raise RuntimeError(
            'theme folders missing\n- "{}"\n- "{}"'.format(stat, tmpl)
        )
    return stat, tmpl


def url_blocklist(base=BLOCK_BASE, filename=BLOCK_FILE):
    location = path.abspath(path.join(base, filename))
    result = []
    if path.exists(location):
        with open(location, 'r') as handle:
            for line in [ln.strip() for ln in handle.readlines()]:
                if line and not line.startswith('#'):
                    result.append(rx_compile(line, IGNORECASE))
    return result


# pylint: disable=too-few-public-methods


class BaseConfig:
    APP_NAME = APP_NAME
    DEBUG = False
    HTML_LANG = HTML_LANG
    PAGINATION = PAGINATION
    SECRET_KEY = secret_key()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    TITLE = TITLE
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = CSRF_STRICT


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_DEV


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE
