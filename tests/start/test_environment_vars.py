from string import ascii_letters, digits, punctuation, whitespace

from shorter.start.environment import (
    APP_NAME, CRAWLERS, ERROR_CODES, MDL_NAME, RX_XSS_STORED, SOCIAL, SYM_MINI,
    SYM_POOL
)


def test_appname():
    assert APP_NAME == 'shorter'


def test_modulename():
    assert MDL_NAME == 'shorter'


def test_symbol_minimum():
    assert SYM_MINI == 3


def test_xss_stored():
    assert RX_XSS_STORED == '.+\\\'\\+.+//'


def test_symbol_pool():
    pool = digits + ascii_letters
    assert len(SYM_POOL) == len(pool)

    for sym in pool:
        assert sym in SYM_POOL
    for n_sym in punctuation + whitespace:
        assert n_sym not in SYM_POOL


def test_errorcodes():
    def _check(start, end=None):
        count = 0
        for code in range(start, 1 + (end if end is not None else start)):
            assert code in ERROR_CODES
            count += 1

        return count

    total = sum([
        _check(400, 401),
        _check(403, 404),
        _check(418),

        _check(500, 504),
    ])
    assert len(ERROR_CODES) == total


def test_bot_and_social():
    for collection in (CRAWLERS, SOCIAL):
        assert collection
        for elem in collection:
            assert elem
            assert isinstance(elem, str)
            assert elem.lower() == elem
