from collections import namedtuple

from flask import url_for
from pytest import fixture
from sqlalchemy.orm import scoped_session, sessionmaker

from shorter.app import create_app
from shorter.start.config import TestingConfig
from shorter.start.extensions import DB as _db

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments


@fixture(scope="session")
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        yield _app


@fixture(scope="function")
def db(app):
    _db.app = app
    _db.create_all()

    yield _db
    _db.session.close()
    _db.drop_all()


@fixture(scope="function")
def session(db):
    _connection = db.engine.connect()
    _session = scoped_session(session_factory=sessionmaker(bind=_connection))
    db.session = _session

    yield _session

    _connection.close()
    _session.remove()


@fixture(scope="session")
def ctx_app(app):
    with app.test_request_context():
        yield app


@fixture(scope="function")
def client(ctx_app):
    with ctx_app.test_client() as cli:
        yield cli


def _visitor(client):
    def visit(
        endpoint,
        *,
        code=200,
        data=None,
        headers=None,
        method="get",
        params=None,
        query_string=None,
    ):
        if params is None:
            params = {}

        url = url_for(endpoint, **params)
        func = {
            "get": client.get,
            "post": client.post,
        }.get(method.lower())

        resp = func(
            url,
            data=data,
            headers=headers,
            query_string=query_string,
        )
        assert resp.status_code == code

        res = {
            "url": url,
            "response": resp,
            "text": resp.get_data(as_text=True),
            "headers": resp.headers,
        }
        return namedtuple("Result", res.keys())(**res)

    return visit


@fixture(scope="function")
def visitor(client):
    yield _visitor(client)
