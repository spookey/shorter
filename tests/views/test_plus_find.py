from flask import url_for
from pytest import mark

from shorter.models.short import Short

ENDPOINT = 'plus.find'


@mark.usefixtures('session')
class TestPlusFind:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/plus/find'

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        assert 'form' in res.text
        assert 'Find' in res.text

    @staticmethod
    def test_search_by_param(visitor):
        assert Short.query.count() == 0
        one = Short.generate(target='___one')
        two = Short.generate(target='two___')
        assert Short.query.count() == 2

        org = visitor(ENDPOINT)
        res_one = visitor(ENDPOINT, query_string='q=one')
        res_two = visitor(ENDPOINT, query_string='q=two')
        res_all = visitor(ENDPOINT, query_string='q=___')
        exp_one = 'value="one"'
        exp_two = 'value="two"'
        exp_all = 'value="___"'

        assert exp_one not in org.text
        assert exp_two not in org.text
        assert exp_all not in org.text

        assert exp_one in res_one.text
        assert one.target in res_one.text

        assert exp_two in res_two.text
        assert two.target in res_two.text

        assert exp_all in res_all.text
        assert one.target in res_all.text
        assert two.target in res_all.text

    @staticmethod
    def test_submit(visitor):
        term = 'whatever'
        res = visitor(ENDPOINT, method='post', data={
            'term': term, 'submit': True,
        }, code=302)
        assert res.url == url_for(ENDPOINT)
        assert res.response.location == url_for(
            ENDPOINT, q=term, _external=True
        )

    @staticmethod
    def test_invalid_param(visitor):
        visitor(ENDPOINT, params={'page': 42}, code=404)
        visitor(ENDPOINT, params={
            'page': 1, 'field': 'eggplant'
        }, code=404)
        visitor(ENDPOINT, params={
            'page': 1, 'field': 'eggplant', 'order': 'sausage'
        }, code=404)
