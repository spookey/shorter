from shorter.start.helper import FALSY, TRUTHY, parse_bool

UNKNOWN = ("", ".", "🧦")
WRONG = (23, None, Exception)


def test_simple():
    for val in TRUTHY:
        assert parse_bool(val, warn=False) is True
    for val in FALSY:
        assert parse_bool(val, warn=False) is False


def test_case_insensitive():
    for val in TRUTHY:
        assert parse_bool(val.upper(), warn=False) is True
    for val in FALSY:
        assert parse_bool(val.upper(), warn=False) is False


def test_fallback():
    for val in WRONG:
        assert parse_bool(val, fallback=True, warn=False) is True
        assert parse_bool(val, fallback=False, warn=False) is False


def test_unknown_fallback():
    for val in UNKNOWN:
        assert parse_bool(val, fallback=True, warn=False) is True
        assert parse_bool(val, fallback=False, warn=False) is False


def test_silent(caplog):
    assert parse_bool(WRONG[-1], fallback=True, warn=False) is True
    assert not caplog.records


def test_logging(caplog):
    assert parse_bool(WRONG[-1], fallback=True, warn=True) is True

    exc, wrn = caplog.records

    assert exc.levelname == "ERROR"
    assert wrn.levelname == "WARNING"

    assert "Exception" in exc.message
    assert "lower" in exc.message
    assert "fallback" in wrn.message
    assert "True" in wrn.message


def test_unknown_logging(caplog):
    assert parse_bool(UNKNOWN[-1], fallback=True, warn=True) is True

    wrn = caplog.records[0]
    assert caplog.records == [wrn]

    assert wrn.levelname == "WARNING"
    assert "fallback" in wrn.message
    assert "True" in wrn.message
