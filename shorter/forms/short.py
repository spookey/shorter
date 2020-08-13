from flask import url_for
from flask_wtf import FlaskForm
from werkzeug.urls import url_fix
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length

from shorter.models.short import Short
from shorter.start.environment import (
    DELAY_DEF, DELAY_MAX, DELAY_MIN, DELAY_STP
)
from shorter.support import BLOCKLIST, BlocklistValidator

MAIN_ENDPOINT = 'main.short'
SHOW_ENDPOINT = 'plus.show'


# pylint: disable=arguments-differ


class ShortCreateForm(FlaskForm):
    target = StringField(
        'Target',
        validators=[
            DataRequired(), Length(min=8), URL(),
            BlocklistValidator(BLOCKLIST),
        ],
        description='Link target',
    )
    delay = SelectField(
        'Delay',
        default=DELAY_DEF,
        coerce=int,
        description='Forward delay in seconds',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
    )

    @staticmethod
    def delay_choices():
        return [
            (num, '{:02d}'.format(num))
            for num in range(DELAY_MIN, 1 + DELAY_MAX, DELAY_STP)
        ]

    def __init__(self, *args, **kwargs):
        super(ShortCreateForm, self).__init__(*args, **kwargs)
        self.delay.choices = self.delay_choices()

    def fix_target(self):
        if isinstance(self.target.data, str):
            self.target.data = self.target.data.strip()
            pre, sep, _ = self.target.data.partition('//')
            if not sep:
                self.target.data = 'http://{}'.format(pre)
            self.target.data = url_fix(self.target.data)

    def validate(self):
        self.fix_target()
        return super(ShortCreateForm, self).validate()

    def action(self):
        if not self.validate():
            return None

        return Short.generate(
            target=self.target.data,
            delay=self.delay.data,
            _commit=True
        )


class ShortDisplayForm(FlaskForm):
    link = StringField(
        'Link',
        render_kw={'readonly': True},
        description='Forwarding link',
    )
    copy = SubmitField(
        'Copy',
        description='Copy to clipboard',
    )

    def __init__(self, *args, obj, **kwargs):
        super(ShortDisplayForm, self).__init__(*args, obj=obj, **kwargs)
        if obj is not None and obj.symbol is not None:
            self.link.data = url_for(
                MAIN_ENDPOINT, symb=obj.symbol, _external=True
            )

    @staticmethod
    def validate():
        return False


class ShortFindForm(FlaskForm):
    term = StringField(
        'Term',
        validators=[DataRequired()],
        description='Search term',
    )
    send = SubmitField(
        'Search',
        description='Search and find',
    )

    def action(self):
        if not self.validate():
            return None

        return url_for(SHOW_ENDPOINT, q=self.term.data)
