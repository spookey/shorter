from flask import url_for
from pytest import mark

from shorter.forms.short import ShortFindForm

ENDPOINT = 'plus.find'

def _phony(term=None):
    def elem():
        pass

    elem.term = term
    return elem


@mark.usefixtures('session', 'ctx_app')
class TestShortFindForm:

    @staticmethod
    def test_fields():
        form = ShortFindForm(obj=None)
        assert form.term.data is None
        assert form.send.data is False

        form = ShortFindForm(obj=_phony())
        assert form.term.data is None
        assert form.send.data is False

    @staticmethod
    def test_field_init():
        form = ShortFindForm(obj=_phony('test'))
        assert form.term.data == 'test'
        assert form.send.data is False

    @staticmethod
    def test_action():
        form = ShortFindForm(term='')
        assert form.action() is None

        form = ShortFindForm(term='🔍')
        rdir = form.action()
        assert rdir == url_for(ENDPOINT, q='🔍')
