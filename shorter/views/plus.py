from flask import Blueprint, abort, current_app, render_template

from shorter.models.short import Short

BLUEPRINT_PLUS = Blueprint('plus', __name__, url_prefix='/plus')


@BLUEPRINT_PLUS.route('/')
def index():
    return render_template(
        'plus/index.html',
        title='Plus'
    )


@BLUEPRINT_PLUS.route('/table/<string:field>/<any(asc,desc):sort>/<int:page>')
@BLUEPRINT_PLUS.route('/table/<string:field>/<int:page>')
@BLUEPRINT_PLUS.route('/table/<int:page>')
@BLUEPRINT_PLUS.route('/table')
def table(page=None, field=None, sort=None):
    query = Short.ordered(
        field=field,
        rev=sort == 'desc'
    )
    if not query:
        abort(404)

    return render_template(
        'plus/table.html',
        title='Table',
        elements=query.paginate(
            page=page, per_page=current_app.config['PAGINATION']
        )
    )
