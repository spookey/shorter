from flask import Flask

from shorter.start.extensions import CSRF_PROTECT, DB, MIGRATE

MODULE = __name__.split('.')[0]


def create_app(config_obj):
    app = Flask(MODULE)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    CSRF_PROTECT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)


def register_errorhandlers(_):
    pass


def register_blueprints(_):
    pass
