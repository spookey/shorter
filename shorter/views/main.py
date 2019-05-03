from flask import Blueprint, abort, current_app, make_response, render_template

from shorter.models.short import Short

BLUEPRINT_MAIN = Blueprint('main', __name__)


@BLUEPRINT_MAIN.route('/')
def index():
    return render_template(
        'index.html',
        title=current_app.config['TITLE']
    )


@BLUEPRINT_MAIN.route('/<symbol:symb>')
def short(symb):
    item = Short.by_symbol(symb)
    if not item:
        abort(404)

    resp = make_response(render_template(
        'short.html',
        title=item.symbol,
        short=item,
    ))

    resp.headers.add('X-Robots-Tag', 'noindex, nofollow')
    return resp
