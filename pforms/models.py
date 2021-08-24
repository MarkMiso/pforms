from .extensions import db, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User: {self.username}>'

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_user_forms(self):
        return Form.query.filter_by(creator=self.id).all()
     
class Form(db.Model):
   __tablename__ = 'forms'
   
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(120), nullable=False)
   description = db.Column(db.String(500), nullable=False)
   creator = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)     
   submit_number = db.Column(db.Integer, default=0)

class Question(db.Model):
   __tablename__ = 'questions'
   
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.String(250), nullable=False)
   category = db.Column(db.String(120), nullable=False)
   form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)     
   multiple = db.Column(db.Boolean)

class Answer(db.Model):
   __tablename__ = 'answers'
   
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.String(250), nullable=False)
   question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)     
   next_question = db.Column(db.Integer, db.ForeignKey('questions.id'))     
   times_selected = db.Column(db.Integer, default=0)