from flask import url_for
from pytest import mark

from shorter.start.config import APP_NAME

ENDPOINT = 'main.index'


@mark.usefixtures('session')
class TestIndex:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/'

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT, 'get')
        assert APP_NAME in res.page
