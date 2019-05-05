from collections import namedtuple

from flask import (
    Blueprint, abort, current_app, make_response, render_template, request
)

from shorter.forms.short import ShortCreateForm, ShortDisplayForm
from shorter.models.short import Short
from shorter.start.environment import DELAY_DEF
from shorter.support import is_botagent

LINK = namedtuple('Link', ('source', 'target'))

BLUEPRINT_MAIN = Blueprint('main', __name__)


@BLUEPRINT_MAIN.route('/', methods=['GET', 'POST'])
def index():
    link = None
    form = ShortCreateForm(
        target=request.args.get('target'),
        delay=request.args.get('delay', DELAY_DEF),
    )
    if form.validate_on_submit():
        obj = form.action()
        if obj:
            form = ShortDisplayForm(obj=obj)
            link = LINK(source=form.link.data, target=obj.target)

    return render_template(
        'index.html',
        title=current_app.config.get('TITLE'),
        form=form,
        link=link,
    )


@BLUEPRINT_MAIN.route('/<symbol:symb>')
def short(symb):
    if is_botagent(request.user_agent):
        abort(403)

    item = Short.by_symbol_active(symb)
    if not item:
        abort(404)

    item.increase_visit()
    resp = make_response(render_template(
        'short.html',
        title=item.symbol,
        short=item,
    ))

    resp.headers.add('X-Robots-Tag', 'noindex, nofollow')
    return resp
