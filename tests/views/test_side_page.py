from flask import url_for
from pytest import mark

ENDPOINT = 'side.page'


@mark.usefixtures('session')
class TestSidePage:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT, name='test') == '/page/test'

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT, params={'name': 'about'})
        assert 'about' in res.text

    @staticmethod
    def test_hidden(visitor):
        res = visitor(ENDPOINT, params={'name': '_base'}, code=404)
        assert '404' in res.text

    @staticmethod
    def test_not_found(visitor):
        res = visitor(ENDPOINT, params={'name': 'test'}, code=404)
        assert '404' in res.text
