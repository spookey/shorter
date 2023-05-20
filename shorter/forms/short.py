from urllib.parse import quote, quote_plus, urlparse, urlunparse

from flask import url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length

from shorter.models.short import Short
from shorter.start.environment import (
    DELAY_DEF,
    DELAY_MAX,
    DELAY_MIN,
    DELAY_STP,
)
from shorter.support import BLOCKLIST, BlocklistValidator

MAIN_ENDPOINT = "main.short"
SHOW_ENDPOINT = "plus.show"


# pylint: disable=arguments-differ


class ShortCreateForm(FlaskForm):
    target = StringField(
        "Target",
        validators=[
            DataRequired(),
            Length(min=8),
            URL(),
            BlocklistValidator(BLOCKLIST),
        ],
        description="Link target",
    )
    delay = SelectField(
        "Delay",
        default=DELAY_DEF,
        coerce=int,
        description="Forward delay in seconds",
    )
    submit = SubmitField(
        "Save",
        description="Submit",
    )

    @staticmethod
    def delay_choices():
        return [
            (num, f"{num:02d}")
            for num in range(DELAY_MIN, 1 + DELAY_MAX, DELAY_STP)
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.delay.choices = self.delay_choices()

    @staticmethod
    def _fix(location):
        url = urlparse(location)
        path = quote(url.path, safe="/%+$!*'(),")
        query = quote_plus(url.query, safe=":&%=+$!*'(),")
        fragment = quote_plus(url.fragment, safe=":&%=+$!*'(),")
        return urlunparse((url.scheme, url.netloc, path, "", query, fragment))

    def fix_target(self):
        if isinstance(self.target.data, str):
            self.target.data = self.target.data.strip()
            pre, sep, _ = self.target.data.partition("//")
            if not sep:
                self.target.data = f"http://{pre}"
            self.target.data = self._fix(self.target.data)

    def validate(self, *args, **kwargs):
        self.fix_target()
        return super().validate(*args, **kwargs)

    def action(self):
        if not self.validate():
            return None

        return Short.generate(
            target=self.target.data, delay=self.delay.data, _commit=True
        )


class ShortDisplayForm(FlaskForm):
    link = StringField(
        "Link",
        render_kw={"readonly": True},
        description="Forwarding link",
    )
    copy = SubmitField(
        "Copy",
        description="Copy to clipboard",
    )

    def __init__(self, *args, obj, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)

        if obj is not None and obj.symbol is not None:
            self.link.data = url_for(
                MAIN_ENDPOINT, symb=obj.symbol, _external=True
            )

    @staticmethod
    def validate():
        return False


class ShortFindForm(FlaskForm):
    term = StringField(
        "Term",
        validators=[DataRequired()],
        description="Search term",
    )
    send = SubmitField(
        "Search",
        description="Search and find",
    )

    def action(self):
        if not self.validate():
            return None

        return url_for(SHOW_ENDPOINT, q=self.term.data)
