from pforms import create_app
from pforms.extensions import db
from pforms.models import User

db.create_all(app=create_app())