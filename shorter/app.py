from flask import Flask

from shorter.shared import errorhandler
from shorter.start.config import ERROR_CODES, theme_folders
from shorter.start.extensions import CSRF_PROTECT, DB, MIGRATE
from shorter.views.main import BLUEPRINT_MAIN

MODULE = __name__.split('.')[0]


def create_app(config_obj):
    stat, tmpl = theme_folders()

    app = Flask(
        MODULE,
        static_folder=stat,
        template_folder=tmpl,
    )
    app.config.from_object(config_obj)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    CSRF_PROTECT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)


def register_errorhandlers(app):
    for code in ERROR_CODES:
        app.errorhandler(code)(errorhandler)


def register_blueprints(app):
    app.register_blueprint(BLUEPRINT_MAIN)
