from pytest import mark

from shorter.forms.short import ShortCreateForm, ShortDisplayForm

EXAMPLE = 'http://www.example.org'


@mark.usefixtures('session', 'ctx_app')
class TestShortDisplayForm:

    @staticmethod
    def test_fields():
        form = ShortDisplayForm()
        assert form.show_target.data is None
        assert form.copy.data is False

        form = ShortDisplayForm(show_target='test')
        assert form.show_target.data == 'test'
        assert form.copy.data is False

    @staticmethod
    def test_target_readonly():
        form = ShortDisplayForm()
        assert form.show_target is not None
        assert form.show_target.render_kw is not None
        assert form.show_target.render_kw.get('readonly') is True

    @staticmethod
    def test_swap():
        this_form = ShortCreateForm(target=EXAMPLE)
        assert this_form.target.data == EXAMPLE

        that_form = ShortDisplayForm.swap(this_form)
        assert that_form.show_target.data == EXAMPLE

    @staticmethod
    def test_validate():
        form = ShortDisplayForm()
        assert form.validate() is False

        form = ShortDisplayForm(show_target=EXAMPLE)
        assert form.validate() is False
