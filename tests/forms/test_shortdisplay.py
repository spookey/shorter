from flask import url_for
from pytest import mark

from shorter.forms.short import ShortDisplayForm

ENDPOINT = "main.short"


def _phony(symbol=None):
    def short():
        pass  # pragma: no cover

    short.symbol = symbol
    return short


@mark.usefixtures("session", "ctx_app")
class TestShortDisplayForm:
    @staticmethod
    def test_fields():
        form = ShortDisplayForm(obj=None)
        assert form.link.data is None
        assert form.copy.data is False

        form = ShortDisplayForm(obj=_phony())
        assert form.link.data is None
        assert form.copy.data is False

    @staticmethod
    def test_field_init():
        form = ShortDisplayForm(obj=_phony("test"))
        assert form.link.data == url_for(ENDPOINT, symb="test", _external=True)
        assert form.copy.data is False

    @staticmethod
    def test_target_readonly():
        form = ShortDisplayForm(obj=_phony())
        assert form.link is not None
        assert form.link.render_kw is not None
        assert form.link.render_kw.get("readonly") is True

    @staticmethod
    def test_validate():
        form = ShortDisplayForm(obj=_phony())
        assert form.validate() is False

        form = ShortDisplayForm(obj=_phony("test"))
        assert form.validate() is False
