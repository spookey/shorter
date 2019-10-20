from flask import (
    Blueprint, abort, current_app, redirect, render_template, request
)

from shorter.forms.short import ShortFindForm
from shorter.models.short import Short
from shorter.support import BLOCKLIST

BLUEPRINT_PLUS = Blueprint('plus', __name__, url_prefix='/plus')


@BLUEPRINT_PLUS.route('/')
def index():
    form = ShortFindForm(
        term=request.args.get('q')
    )

    return render_template(
        'plus/index.html',
        title='Plus',
        form=form,
    )


@BLUEPRINT_PLUS.route('/table/<string:field>/<any(asc,desc):sort>/<int:page>')
@BLUEPRINT_PLUS.route('/table/<string:field>/<int:page>')
@BLUEPRINT_PLUS.route('/table/<int:page>')
@BLUEPRINT_PLUS.route('/table')
def table(page=None, field=None, sort=None):
    query = Short.ordered(field=field, rev=sort == 'desc')
    if not query:
        abort(404)

    return render_template(
        'plus/table.html',
        title='Table',
        elements=query.paginate(
            page=page, per_page=current_app.config['PAGINATION']
        )
    )


@BLUEPRINT_PLUS.route(
    '/find/<string:field>/<any(asc,desc):sort>/<int:page>',
    methods=['POST', 'GET']
)
@BLUEPRINT_PLUS.route(
    '/find/<string:field>/<int:page>',
    methods=['POST', 'GET']
)
@BLUEPRINT_PLUS.route('/find/<int:page>', methods=['POST', 'GET'])
@BLUEPRINT_PLUS.route('/find', methods=['POST', 'GET'])
def find(page=None, field=None, sort=None):
    form = ShortFindForm(term=request.args.get('q'))
    if form.validate_on_submit():
        target = form.action()
        if target:
            return redirect(target)

    query = Short.searched(form.term.data, field=field, rev=sort == 'desc')
    if not query:
        abort(404)

    return render_template(
        'plus/table.html',
        title='Find',
        form=form,
        elements=query.paginate(
            page=page, per_page=current_app.config['PAGINATION']
        ),
    )


@BLUEPRINT_PLUS.route('/block/<string:field>/<any(asc,desc):sort>/<int:page>')
@BLUEPRINT_PLUS.route('/block/<string:field>/<int:page>')
@BLUEPRINT_PLUS.route('/block/<int:page>')
@BLUEPRINT_PLUS.route('/block')
def block(page=None, field=None, sort=None):
    query = Short.blocked(BLOCKLIST, field=field, rev=sort == 'desc')
    if not query:
        abort(404)

    return render_template(
        'plus/table.html',
        title='Blocked',
        elements=query.paginate(
            page=page, per_page=current_app.config['PAGINATION']
        )
    )
