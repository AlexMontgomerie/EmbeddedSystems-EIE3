from flask import Flask
from flask import url_for, render_template
from werkzeug.contrib.fixers import ProxyFix
from raven.contrib.flask import Sentry

# setup logging
import logging

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger("web")
logger.addHandler(handler)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(handler)

import os
basedir = os.path.abspath(os.path.dirname(__file__))

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def create_app(config_name):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    from .landing import landing as landing_blueprint
    app.register_blueprint(landing_blueprint)

    from .templates import templates as templates_blueprint
    app.register_blueprint(templates_blueprint)

    @app.before_first_request
    def setup_logging():
        if not app.debug:
            app.logger.addHandler(handler)
    return app
