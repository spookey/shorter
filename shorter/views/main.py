from flask import Blueprint, current_app, render_template

BLUEPRINT_MAIN = Blueprint('main', __name__)


@BLUEPRINT_MAIN.route('/index')
@BLUEPRINT_MAIN.route('/')
def index():
    return render_template(
        'index.html',
        title=current_app.config['APP_NAME']
    )
