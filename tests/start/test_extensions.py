from pytest import mark

from shorter.start.extensions import CSRF_PROTECT, DB


@mark.usefixtures("app")
class TestExtensions:
    @staticmethod
    def test_for_csrf(app):
        assert CSRF_PROTECT is not None
        assert CSRF_PROTECT == app.extensions["csrf"]
        assert app.config["WTF_CSRF_CHECK_DEFAULT"] is True

    @staticmethod
    def test_for_db():
        assert DB is not None
        assert DB.engine.url.database is None  # memory db
