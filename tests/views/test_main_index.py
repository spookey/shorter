from flask import url_for
from pytest import mark

from shorter.models.short import Short
from shorter.start.environment import DELAY_STP, TITLE

ENDPOINT = "main.index"
EXAMPLE = "http://www.example.org"


@mark.usefixtures("session")
class TestMainIndex:
    @staticmethod
    @mark.usefixtures("ctx_app")
    def test_url():
        assert url_for(ENDPOINT) == "/"

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        assert TITLE in res.text
        assert "form" in res.text

    @staticmethod
    def test_urlparams(visitor):
        """may break depending on theme"""
        org = visitor(ENDPOINT)

        res = visitor(ENDPOINT, query_string=f"target={EXAMPLE}")
        exp = f'value="{EXAMPLE}"'
        assert exp not in org.text
        assert exp in res.text

        res = visitor(ENDPOINT, query_string=f"delay={DELAY_STP}")
        exp = f'selected value="{DELAY_STP}"'
        assert exp not in org.text
        assert exp in res.text

    @staticmethod
    def test_fill_wrong(visitor):
        assert Short.query.count() == 0
        visitor(
            ENDPOINT,
            method="post",
            data={
                "target": "...",
                "delay": 1337,
                "submit": True,
            },
        )
        assert Short.query.count() == 0

    @staticmethod
    def test_fill(visitor):
        assert Short.query.count() == 0
        res = visitor(
            ENDPOINT,
            method="post",
            data={
                "target": EXAMPLE,
                "delay": 2 * DELAY_STP,
                "submit": True,
            },
        )

        obj = Short.query.first()
        assert obj.target == EXAMPLE

        assert (
            url_for("main.short", symb=obj.symbol, _external=True) in res.text
        )
