from re import IGNORECASE
from re import compile as re_compile

from pytest import mark

from shorter.forms.short import ShortCreateForm
from shorter.start.environment import (
    DELAY_DEF,
    DELAY_MAX,
    DELAY_MIN,
    DELAY_STP,
)
from shorter.support import BlocklistValidator

EXAMPLE = "http://www.example.org"


@mark.usefixtures("session", "ctx_app")
class TestShortCreateForm:
    @staticmethod
    def test_fields():
        form = ShortCreateForm()
        assert form.target.data is None
        assert form.delay.data == DELAY_DEF
        assert form.submit.data is False

        form = ShortCreateForm(target="test", delay=23)
        assert form.target.data == "test"
        assert form.delay.data == 23
        assert form.submit.data is False

    @staticmethod
    def test_delay_choices():
        form = ShortCreateForm()
        choices = form.delay_choices()
        for num, txt in choices:
            assert num >= DELAY_MIN
            assert num <= DELAY_MAX
            assert str(num) in txt

    @staticmethod
    def test_fix_target():
        form = ShortCreateForm()
        assert form.target.data is None

        form.fix_target()
        assert form.target.data is None

        form.target.data = EXAMPLE
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = EXAMPLE.replace("http://", "")
        form.fix_target()
        assert form.target.data == EXAMPLE

    @staticmethod
    def test_fix_target_special():
        form = ShortCreateForm()
        assert form.target.data is None

        form.target.data = f"\t{EXAMPLE}    "
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = f"    {EXAMPLE}\t"
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = "https://💩.la"
        form.fix_target()
        assert form.target.data == "https://💩.la"  # xn--ls8h.la

        form.target.data = "http://localhost/‼️?🫵=🥔"
        form.fix_target()
        assert (
            form.target.data
            == "http://localhost/%E2%80%BC%EF%B8%8F?%F0%9F%AB%B5=%F0%9F%A5%94"
        )

        form.target.data = f"{EXAMPLE}/ (äöüß)"
        form.fix_target()
        assert form.target.data == f"{EXAMPLE}/%20(%C3%A4%C3%B6%C3%BC%C3%9F)"

        form.target.data = f"{EXAMPLE}/<script>alert(1);</script>"
        form.fix_target()
        assert form.target.data == (
            f"{EXAMPLE}/%3Cscript%3Ealert(1)%3B%3C/script%3E"
        )

    @staticmethod
    def test_validate():
        form = ShortCreateForm(target="🚫")
        assert form.validate() is False

        form = ShortCreateForm(target=EXAMPLE)
        assert form.validate() is True

    @staticmethod
    def test_action():
        form = ShortCreateForm(target="🚫")
        assert form.action() is None

        form = ShortCreateForm(target=EXAMPLE, delay=3 * DELAY_STP)
        obj = form.action()
        assert obj is not None
        assert obj.target == EXAMPLE
        assert obj.symbol
        assert obj.delay == 3 * DELAY_STP

    @staticmethod
    def test_blocklisted():
        validator = BlocklistValidator(
            [re_compile(r"^.+example\.com$", IGNORECASE)]
        )

        def _inject(form):
            form.target.validators = [
                val if isinstance(val, type(validator)) else validator
                for val in form.target.validators
            ]

        form = ShortCreateForm(target="https://example.org")
        _inject(form)
        assert form.validate() is True

        form = ShortCreateForm(target="https://example.com")
        _inject(form)
        assert form.validate() is False

    @staticmethod
    def test_blocklisted_stored_xss():
        xss = """https://example.org'+alert('xss'))//"""

        form = ShortCreateForm(target=xss)
        assert form.validate() is False
