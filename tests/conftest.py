from collections import namedtuple

from flask import url_for
from pytest import fixture, mark

from shorter.app import create_app
from shorter.start.config import TestingConfig
from shorter.start.extensions import DB as _db

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments


def pytest_addoption(parser):
    parser.addoption(
        '--runslow', action='store_true', default=False, help='run slow tests'
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = mark.skip(reason='needs --runslow to run')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow)


@fixture(scope='session')
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        yield _app


@fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db
    _db.session.close()
    _db.drop_all()


@fixture(scope='function')
def session(db):
    _connection = db.engine.connect()
    _transaction = _connection.begin()
    _session = db.create_scoped_session(
        options={'bind': _connection, 'binds': {}}
    )
    db.session = _session

    yield _session
    _transaction.rollback()
    _connection.close()
    _session.remove()


@fixture(scope='session')
def ctx_app(app):
    with app.test_request_context():
        yield app


@fixture(scope='function')
def client(ctx_app):
    cli = ctx_app.test_client()
    with cli:
        yield cli


def _visitor(client):
    def visit(
            endpoint, params=None, method='get', code=200
    ):
        if params is None:
            params = {}

        url = url_for(endpoint, **params)
        func = {
            'get': client.get,
            'post': client.post,
        }.get(method.lower())

        resp = func(url)
        assert resp.status_code == code

        res = {
            'url': url,
            'resp': resp,
            'text': resp.get_data(as_text=True)
        }
        return namedtuple('Result', res.keys())(**res)

    return visit


@fixture(scope='function')
def visitor(client):
    yield _visitor(client)
