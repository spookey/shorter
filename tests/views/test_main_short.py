from random import choice

from flask import url_for
from pytest import mark

from shorter.models.short import Short
from shorter.start.environment import SYM_MINI, SYM_POOL

ENDPOINT = 'main.short'


def _sym():
    return ''.join(choice(SYM_POOL) for _ in range(SYM_MINI))


@mark.usefixtures('session')
class TestShort:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        sym = _sym()
        assert url_for(ENDPOINT, symb=sym) == '/{}'.format(sym)

    @staticmethod
    def test_not_found(visitor):
        sym = _sym()
        res = visitor(ENDPOINT, params={'symb': sym}, code=404)

        assert res.url == '/{}'.format(sym)

    @staticmethod
    def test_basic_view(visitor):
        sym = _sym()
        tgt = 'demo test'
        Short.create(symbol=sym, target=tgt)
        res = visitor(ENDPOINT, params={'symb': sym})

        assert res.url == '/{}'.format(sym)
        assert tgt in res.text

    @staticmethod
    def test_headers(visitor):
        sym = _sym()
        Short.create(symbol=sym, target='test demo')
        res = visitor(ENDPOINT, params={'symb': sym})

        robots = res.headers.get('X-Robots-Tag')
        assert robots
        assert 'noindex' in robots.lower()
        assert 'nofollow' in robots.lower()
