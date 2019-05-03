from flask import url_for
from pytest import mark

from shorter.start.environment import TITLE

ENDPOINT = 'main.index'


@mark.usefixtures('session')
class TestIndex:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/'

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT, method='get')
        assert TITLE in res.text
