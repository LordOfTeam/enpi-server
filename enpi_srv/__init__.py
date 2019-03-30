import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from .extensions import rest_api, mail
from enpi_srv.controllers import core_blueprint
from enpi_srv.controllers.rest.tickets import TicketFormView, SMSSecurityCode


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True)

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('enpi_srv.config.DevConfig')
    else:
        app.config.from_object('enpi_srv.config.PrdConfig')

    # Onput Log
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    if app.debug:
        handler = logging.StreamHandler()
    else:
        handler = RotatingFileHandler('/tmp/enpi_srv.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.NOTSET)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    rest_api.add_resource(
        TicketFormView,
        '/core/apply',
        endpoint='create-apply'
    )
    rest_api.add_resource(
        SMSSecurityCode,
        '/core/acscode',
        endpoint='acscode'
    )

    rest_api.init_app(app)
    mail.init_app(app)

    app.register_blueprint(core_blueprint)

    return app
