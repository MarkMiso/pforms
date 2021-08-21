from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()