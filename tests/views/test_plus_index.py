from flask import url_for
from pytest import mark

ENDPOINT = "plus.index"


@mark.usefixtures("session")
class TestPlusIndex:
    @staticmethod
    @mark.usefixtures("ctx_app")
    def test_url():
        assert url_for(ENDPOINT) == "/plus/"

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        assert "Plus" in res.text
        assert "Table" in res.text
        assert "Find" in res.text
        assert "form" in res.text
