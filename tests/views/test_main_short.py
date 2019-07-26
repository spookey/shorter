from random import choice

from flask import url_for
from pytest import mark

from shorter.models.short import Short
from shorter.start.environment import SYM_MINI, SYM_POOL

ENDPOINT = 'main.short'


def _sym():
    return ''.join(choice(SYM_POOL) for _ in range(SYM_MINI))


def _sho(target='test'):
    return Short.create(symbol=_sym(), target=target)


@mark.usefixtures('session')
class TestMainShort:

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
        sho = _sho()
        res = visitor(ENDPOINT, params={'symb': sho.symbol})

        assert res.url == '/{}'.format(sho.symbol)
        assert sho.target in res.text

    @staticmethod
    def test_headers(visitor):
        sho = _sho()
        res = visitor(ENDPOINT, params={'symb': sho.symbol})

        robots = res.headers.get('X-Robots-Tag')
        assert robots
        assert 'noindex' in robots.lower()
        assert 'nofollow' in robots.lower()

    @staticmethod
    def test_crawler(visitor):
        sho = _sho()
        res = visitor(ENDPOINT, params={'symb': sho.symbol}, headers={
            'User-Agent': 'yandex'
        }, code=403)

        assert res.response.status_code == 403
