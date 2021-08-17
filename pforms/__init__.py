from flask import Flask

from .extensions import db
from .site.routes import site
from .api.routes import api

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(site)
    app.register_blueprint(api)

    return app