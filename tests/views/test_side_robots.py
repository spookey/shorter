from flask import url_for
from pytest import mark

ENDPOINT = 'side.robots'
EP_INDEX = 'main.index'
EP_SHORT = 'main.short'


@mark.usefixtures('session')
class TestRobots:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/robots.txt'

    @staticmethod
    def test_basic_view(visitor):
        idx = url_for(EP_INDEX)
        sht = url_for(EP_SHORT, symb='')

        res = visitor(ENDPOINT)
        assert 'user-agent: *' in res.text.lower()
        assert 'allow: {}$'.format(idx) in res.text.lower()
        assert 'disallow: {}'.format(sht) in res.text.lower()

    @staticmethod
    def test_headers(visitor):
        res = visitor(ENDPOINT)
        assert 'text/plain' in res.headers.get('content-type')
