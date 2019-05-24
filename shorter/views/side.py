from flask import (
    Blueprint, abort, current_app, make_response, render_template,
    send_from_directory, url_for
)
from jinja2.exceptions import TemplateNotFound

BLUEPRINT_SIDE = Blueprint('side', __name__)


@BLUEPRINT_SIDE.route('/robots.txt')
def robots():
    resp = make_response('''
User-Agent: *
Allow: {index}$
Allow: {favicon}
Disallow: {short}
    '''.format(
        index=url_for('main.index'),
        favicon=url_for('side.favicon'),
        short=url_for('main.short', symb=''),
    ).strip())

    resp.headers.set('Content-Type', 'text/plain', charset='utf-8')
    return resp


@BLUEPRINT_SIDE.route('/logo.png', endpoint='logo')
@BLUEPRINT_SIDE.route('/favicon.ico')
@BLUEPRINT_SIDE.route('/favicon.png')
def favicon():
    return send_from_directory(
        current_app.static_folder,
        'favicon.png',
        mimetype='image/png',
    )


@BLUEPRINT_SIDE.route('/page/<string:name>')
def page(name):
    try:
        return render_template(
            'page/{}.html'.format(name),
            title=name,
        )
    except TemplateNotFound:
        abort(404)
