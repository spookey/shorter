from pytest import mark

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

        form.target.data = '\t{}    '.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = '{}/'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

        form.target.data = '    {}///\t'.format(EXAMPLE)
        form.fix_target()
        assert form.target.data == EXAMPLE

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
