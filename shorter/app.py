from flask import Flask

from shorter.shared import (
    bookmarklet, clipboard_copy, errorhandler, redirect_link, redirect_meta,
    redirect_script
)
from shorter.start.config import theme_folders
from shorter.start.environment import ERROR_CODES, MDL_NAME
from shorter.start.extensions import CSRF_PROTECT, DB, MIGRATE
from shorter.start.logger import initialize_logging
from shorter.support import SymbolConverter, is_botagent, is_socialagent
from shorter.views.main import BLUEPRINT_MAIN
from shorter.views.plus import BLUEPRINT_PLUS
from shorter.views.side import BLUEPRINT_SIDE

STATIC, TEMPLATE = theme_folders()


def create_app(config_obj):
    initialize_logging()

    app = Flask(
        MDL_NAME,
        static_folder=STATIC,
        template_folder=TEMPLATE,
    )
    app.config.from_object(config_obj)

    register_extensions(app)
    register_converters(app)
    register_errorhandlers(app)
    register_blueprints(app)
    register_template_functions(app)

    return app


def register_extensions(app):
    CSRF_PROTECT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)


def register_converters(app):
    app.url_map.converters.update(symbol=SymbolConverter)


def register_errorhandlers(app):
    for code in ERROR_CODES:
        app.errorhandler(code)(errorhandler)


def register_blueprints(app):
    app.register_blueprint(BLUEPRINT_MAIN)
    app.register_blueprint(BLUEPRINT_SIDE)
    app.register_blueprint(BLUEPRINT_PLUS)


def register_template_functions(app):
    app.jinja_env.globals.update(
        bookmarklet=bookmarklet,
        clipboard_copy=clipboard_copy,
        is_botagent=is_botagent,
        is_socialagent=is_socialagent,
        redirect_link=redirect_link,
        redirect_meta=redirect_meta,
        redirect_script=redirect_script,
    )
