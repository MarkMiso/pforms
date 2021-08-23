from flask import Flask

from .extensions import db, login_manager
from .site.user import user
from .site.form import form

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    login_manager.init_app(app)
    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(form)

    return app