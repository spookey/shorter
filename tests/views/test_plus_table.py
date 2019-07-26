from flask import url_for
from pytest import mark

from shorter.models.short import Short

ENDPOINT = 'plus.table'


@mark.usefixtures('session')
class TestPlusTable:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/plus/table'

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        assert 'Table' in res.text

    @staticmethod
    def test_content(visitor):
        assert Short.query.count() == 0
        obj = Short.create(symbol='symbol', target='target')

        res = visitor(ENDPOINT)
        txt = res.text
        assert str(obj.prime) in txt
        assert obj.symbol in txt
        assert obj.target in txt
        assert str(obj.created) in txt

    @staticmethod
    def test_first_page(visitor):
        nil = visitor(ENDPOINT)
        one = visitor(ENDPOINT, params={'page': 1})
        assert nil.text == one.text

    @staticmethod
    def test_invalid_param(visitor):
        visitor(ENDPOINT, params={'page': 23}, code=404)
        visitor(ENDPOINT, params={
            'page': 1, 'field': 'banana'
        }, code=404)
        visitor(ENDPOINT, params={
            'page': 1, 'field': 'banana', 'order': 'sausage'
        }, code=404)
