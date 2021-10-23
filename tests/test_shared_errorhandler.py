from pytest import mark
from werkzeug.exceptions import NotFound

from shorter.shared import errorhandler
from shorter.start.environment import ERROR_CODES


def test_app_spec(app):
    for code, mapping in app.error_handler_spec[None].items():
        assert code in ERROR_CODES
        for handler in mapping.values():
            assert handler is errorhandler


@mark.usefixtures("ctx_app")
def test_emitter():
    res, code = errorhandler(NotFound("TEST ERROR"))

    assert "TEST ERROR" in res
    assert code == 404
