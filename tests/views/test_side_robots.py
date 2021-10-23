from random import choice

from flask import url_for
from pytest import mark

from shorter.start.environment import CRAWLERS

ENDPOINT = "side.robots"
EP_FVICO = "side.favicon"
EP_IMAGE = "side.logo"
EP_INDEX = "main.index"
EP_PAGES = "side.page"
EP_SHORT = "main.short"


@mark.usefixtures("session")
class TestSideRobots:
    @staticmethod
    @mark.usefixtures("ctx_app")
    def test_url():
        assert url_for(ENDPOINT) == "/robots.txt"

    @staticmethod
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        txt = res.text.lower()

        assert "user-agent: *" in txt
        assert f"allow: {url_for(EP_INDEX)}$" in txt
        assert f"allow: {url_for(EP_FVICO)}" in txt
        assert f"allow: {url_for(EP_IMAGE)}" in txt
        assert f"allow: {url_for(EP_PAGES, name='')}" in txt

    @staticmethod
    def test_crawler_view(visitor):
        res = visitor(ENDPOINT, headers=[("User-Agent", choice(CRAWLERS))])
        txt = res.text.lower()

        assert "user-agent: *" in txt
        assert f"disallow: {url_for(EP_SHORT, symb='')}" in txt

    @staticmethod
    def test_headers(visitor):
        res = visitor(ENDPOINT)
        assert "text/plain" in res.headers.get("content-type")
