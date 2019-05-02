from flask import (
    Blueprint, current_app, make_response, send_from_directory, url_for
)

BLUEPRINT_SIDE = Blueprint('side', __name__)


@BLUEPRINT_SIDE.route('/robots.txt')
def robots():
    resp = make_response('''
User-Agent: *
Allow: {index}$
Disallow: {short}
    '''.format(
        index=url_for('main.index'),
        short=url_for('main.short', symb=''),
    ).strip())

    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'

    return resp


@BLUEPRINT_SIDE.route('/favicon.ico')
@BLUEPRINT_SIDE.route('/favicon.png')
def favicon():
    return send_from_directory(
        current_app.static_folder,
        'favicon.png',
        mimetype='image/png',
    )
