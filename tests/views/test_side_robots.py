from flask import url_for
from pytest import mark

ENDPOINT = 'side.robots'
EP_FVICO = 'side.favicon'
EP_INDEX = 'main.index'
EP_PAGES = 'side.page'
EP_SHORT = 'main.short'


@mark.usefixtures('session')
class TestRobots:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/robots.txt'

    @staticmethod
    def test_basic_view(visitor):
        fav = url_for(EP_FVICO)
        idx = url_for(EP_INDEX)
        pge = url_for(EP_PAGES, name='')
        sht = url_for(EP_SHORT, symb='')

        res = visitor(ENDPOINT)
        txt = res.text.lower()
        assert 'user-agent: *' in txt
        assert 'allow: {}$'.format(idx) in txt
        assert 'allow: {}'.format(fav) in txt
        assert 'allow: {}'.format(pge) in txt
        assert 'disallow: {}'.format(sht) in txt

    @staticmethod
    def test_headers(visitor):
        res = visitor(ENDPOINT)
        assert 'text/plain' in res.headers.get('content-type')
