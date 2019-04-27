from pytest import fixture

from shorter.app import create_app
from shorter.config import TestingConfig
from shorter.extensions import DB as _db

# pylint: disable=redefined-outer-name,no-member


@fixture(scope='session')
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        yield _app


@fixture(scope='session')
def d_b(app):
    _db.app = app
    _db.create_all()

    yield _db
    _db.session.close()
    _db.drop_all()
