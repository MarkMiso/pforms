from os import path, remove
from .settings import CSV_FOLDER_PATH
from .extensions import db, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    forms = db.relationship('Form', backref='creator', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
       return f'<User: {self.username}>'

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def delete(self):
        for form in self.forms:
            form.delete()

        deleted = User.query.filter_by(email='deleted').first()
        for submission in Submission.query.filter_by(user_id=self.id).all():
            submission.user_id = deleted.id

        db.session.delete(self)
     

class Form(db.Model):
    __tablename__ = 'forms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    questions = db.relationship('Question', backref='form', foreign_keys='Question.form_id', lazy=True)

    def number_of_submissions(self):
        return Submission.query.filter_by(form_id=self.id).count()

    def delete(self):
        # cvs cleaning
        full_path = CSV_FOLDER_PATH + str(self.id) + '.csv'
        
        if path.exists(full_path):
            remove(full_path)

        # submissions deletion
        submissions = Submission.query.filter_by(form_id=self.id).all()
        for submission in submissions:
            submission.delete()
        
        # questions (and answers) deletion
        for question in self.questions:
            question.delete()

        # form deletion
        db.session.delete(self)


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    dependency_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=True)
    multiple = db.Column(db.Boolean, nullable=False)
    
    answers = db.relationship('Answer', backref='question', foreign_keys='Answer.question_id', lazy=True)

    def number_of_answers(self):
        return len(self.answers)

    def delete(self):
        # answers deletion
        for answer in self.answers:
            answer.delete()

        # question deletion
        db.session.delete(self)
        

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    times_selected = db.Column(db.Integer, default=0)

    dependency = db.relationship('Question', backref='dependent', foreign_keys='Question.dependency_id',  lazy=True)

    def get_percent(self):
        form_id = Question.query.filter_by(id=self.question_id).first().form_id
        return int((self.times_selected / Form.query.filter_by(id=form_id).first().number_of_submissions()) * 100)

    def delete(self):
        # delete dependencies 
        for dependency in self.dependency:
            dependency.delete()

        db.session.delete(self)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def delete(self):
        db.session.delete(self)
         

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    forms = db.relationship('Form', backref='category', lazy=True)