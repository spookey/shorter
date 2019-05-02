from os import path, urandom

from shorter.start.environment import (
    DATABASE, DATABASE_DEV, ROOT_DIR, SECRET_BASE, SECRET_FILE, THEME, TITLE
)


def secret_key(base, filename):
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


# pylint: disable=too-few-public-methods


class BaseConfig:
    DEBUG = False
    SECRET_KEY = secret_key(SECRET_BASE, SECRET_FILE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    TITLE = TITLE
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_DEV


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE
