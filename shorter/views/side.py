from flask import (
    Blueprint, abort, current_app, make_response, render_template, request,
    send_from_directory, url_for
)
from jinja2.exceptions import TemplateNotFound

from shorter.support import is_botagent

BLUEPRINT_SIDE = Blueprint('side', __name__)


@BLUEPRINT_SIDE.route('/robots.txt')
def robots():
    cont = [
        'User-Agent: *',
        'Allow: {}$'.format(url_for('main.index')),
        'Allow: {}'.format(url_for('side.favicon')),
        'Allow: {}'.format(url_for('side.logo')),
        'Allow: {}'.format(url_for('side.page', name='')),
    ]
    if is_botagent(request.user_agent):
        cont.append('Disallow: {}'.format(url_for('main.short', symb='')))

    resp = make_response('\n'.join(cont).strip())

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
