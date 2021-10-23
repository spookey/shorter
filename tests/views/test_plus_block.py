from re import IGNORECASE
from re import compile as re_compile

from flask import url_for
from pytest import mark

from shorter.models.short import Short
from shorter.views import plus

ENDPOINT = "plus.block"


@mark.usefixtures("session")
class TestPlusBlock:
    @staticmethod
    @mark.usefixtures("ctx_app")
    def test_url():
        assert url_for(ENDPOINT) == "/plus/block"

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        assert "Blocked" in res.text

    @staticmethod
    def test_display(visitor, monkeypatch):
        assert Short.query.count() == 0
        one = Short.generate(target="one")
        two = Short.generate(target="two")
        thr = Short.generate(target="three")
        assert Short.query.count() == 3

        org = visitor(ENDPOINT)
        blocklist = [re_compile(r"^t.+", IGNORECASE)]
        monkeypatch.setattr(plus, "BLOCKLIST", blocklist)
        res = visitor(ENDPOINT)

        assert "nothing there" in org.text.lower()
        assert "nothing there" not in res.text.lower()
        assert f"<td>{one.prime}</td>" not in res.text
        assert f"<td>{two.prime}</td>" in res.text
        assert f"<td>{thr.prime}</td>" in res.text
        assert one.target not in res.text
        assert two.target in res.text
        assert thr.target in res.text

    @staticmethod
    def test_invalid_param(visitor):
        visitor(
            ENDPOINT,
            params={"page": 1337},
            code=404,
        )
        visitor(
            ENDPOINT,
            params={"page": 1, "field": "peach"},
            code=404,
        )
        visitor(
            ENDPOINT,
            params={"page": 1, "field": "peach", "order": "sausage"},
            code=404,
        )
