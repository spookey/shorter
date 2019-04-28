from pytest import mark

from shorter.start.environment import MIGR_DIR
from shorter.start.extensions import CSRF_PROTECT, DB, MIGRATE


@mark.usefixtures('app')
class TestExtensions:

    @staticmethod
    def test_for_csrf(app):
        assert CSRF_PROTECT is not None
        assert CSRF_PROTECT == app.extensions['csrf']
        assert app.config['WTF_CSRF_CHECK_DEFAULT'] is True

    @staticmethod
    def test_for_db():
        assert DB is not None
        assert DB.engine.url.database is None  # memory db

    @staticmethod
    def test_for_migrate(app, db):
        assert MIGRATE is not None
        assert MIGRATE == app.extensions['migrate'].migrate
        assert MIGRATE.directory == MIGR_DIR
        assert MIGRATE.db == db
