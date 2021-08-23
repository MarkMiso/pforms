from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user
from pforms.models import User

site = Blueprint('site', __name__)

# Login manager loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# Index
@site.route('/')
def index():
    return render_template("index.html")

# User stuff
@site.route('/users/<username>')
@login_required
def show_user(username):
    return render_template('profile.html', user=username)

@site.route('/signup', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password2')

        if password_check == password:
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('username or email already used')
            else:
                user = User(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect(url_for('site.show_user', username=username))
        else:
            flash('passowrds do not match')
        
        return redirect(url_for('site.add_user'))

@site.route('/users/<username>/delete')
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    flash('Success! Your user has been deleted.')
    return render_template('success.html')

# Sign in and sign out
@site.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('site.show_user', username=username))
        else:
            flash('wrong username or password')
            return redirect(url_for('site.signin'))

@site.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('site.index'))

# Forms stuff

@site.route('/forms/creation', methods=['GET', 'POST'])
@login_required
def add_form():
    if request.method == 'GET':
        return render_template('formCreation.html')
    else:
        title = resquest.form.get('title')
        description = request.form.description('derscription')

        return render_template('formCreation.html')