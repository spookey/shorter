from string import digits, punctuation

from shorter.start.helper import parse_int


def test_simple():
    for num in digits:
        assert parse_int(num, warn=False) == int(num)


def test_fallback():
    for pun in punctuation:
        assert parse_int(pun, fallback=23, warn=False) == 23


def test_silent(caplog):
    assert parse_int(None, fallback=42, warn=False) == 42
    assert not caplog.records


def test_logging(caplog):
    assert parse_int(None, fallback=1337, warn=True) == 1337

    exc, wrn = caplog.records
    assert exc.levelname == "ERROR"
    assert wrn.levelname == "WARNING"

    assert "NoneType" in exc.message
    assert "fallback" in wrn.message
    assert "1337" in wrn.message
