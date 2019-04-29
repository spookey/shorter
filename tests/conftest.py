from bs4 import BeautifulSoup
from flask import url_for
from pytest import fixture

from shorter.app import create_app
from shorter.start.config import TestingConfig
from shorter.start.extensions import DB as _db

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments


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
            endpoint, method, param=None,
            data=None, query_string=None,
            code=200
    ):
        if param is None:
            param = dict()

        url = url_for(endpoint, **param)
        request = {
            'get': client.get,
            'post': client.post,
        }.get(method.lower())(
            url, data=data, query_string=query_string
        )
        assert request.status_code == code

        def res():
            pass

        res.url = url
        res.request = request
        res.page = request.get_data(as_text=True)
        res.soup = BeautifulSoup(res.page, 'html.parser')
        return res

    return visit


@fixture(scope='function')
def visitor(client):
    yield _visitor(client)
