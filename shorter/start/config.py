from os import path, urandom

from shorter.start.environment import (
    DATABASE, DATABASE_DEV, SECRET_BASE, SECRET_FILE
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


# pylint: disable=too-few-public-methods


class BaseConfig:
    APP_NAME = 'shorter'
    DEBUG = False
    SECRET_KEY = secret_key(SECRET_BASE, SECRET_FILE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_DEV


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE
