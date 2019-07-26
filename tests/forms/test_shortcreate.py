from re import IGNORECASE
from re import compile as re_compile

from pytest import mark, raises
from wtforms.validators import ValidationError

from shorter.forms.short import ShortCreateForm
from shorter.start.environment import (
    DELAY_DEF, DELAY_MAX, DELAY_MIN, DELAY_STP
)

EXAMPLE = 'http://www.example.org'


@mark.usefixtures('session', 'ctx_app')
class TestShortCreateForm:

    @staticmethod
    def test_fields():
        form = ShortCreateForm()
        assert form.target.data is None
        assert form.delay.data == DELAY_DEF
        assert form.submit.data is False

        form = ShortCreateForm(target='test', delay=23)
        assert form.target.data == 'test'
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

        form.target.data = EXAMPLE.replace('http://', '')
        form.fix_target()
        assert form.target.data == EXAMPLE

    @staticmethod
    def test_fix_target_special():
        form = ShortCreateForm()
        assert form.target.data is None

        form.target.data = '\t{}    '.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = '{}/'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = '    {}///\t'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = 'https://💩.la'
        form.fix_target()
        assert form.target.data == 'https://xn--ls8h.la'

        form.target.data = '{}/ (äöüß)'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == '{}/%20(%C3%A4%C3%B6%C3%BC%C3%9F)'.format(
            EXAMPLE
        )

        form.target.data = '{}/<script>alert(1);</script>'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == '{}/{}'.format(
            EXAMPLE, '%3Cscript%3Ealert(1)%3B%3C/script%3E'
        )

    @staticmethod
    def test_validate():
        form = ShortCreateForm(target='🚫')
        assert form.validate() is False

        form = ShortCreateForm(target=EXAMPLE)
        assert form.validate() is True

    @staticmethod
    def test_action():
        form = ShortCreateForm(target='🚫')
        assert form.action() is None

        form = ShortCreateForm(target=EXAMPLE, delay=3 * DELAY_STP)
        obj = form.action()
        assert obj is not None
        assert obj.target == EXAMPLE
        assert obj.symbol
        assert obj.delay == 3 * DELAY_STP

    @staticmethod
    def test_blocklisted():
        rules = [re_compile(r'^.+example\.com$', IGNORECASE)]

        form = ShortCreateForm(target='https://example.org')
        assert form.check_blocked(blocklist=rules) is None

        form = ShortCreateForm(target='https://example.com')
        with raises(ValidationError) as verr:
            form.check_blocked(blocklist=rules)
            assert 'not possible' in verr.message.lower()
