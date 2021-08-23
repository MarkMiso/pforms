from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user
from pforms.models import User

user = Blueprint('user', __name__)

# Login manager loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# Index
@user.route('/')
def index():
    return render_template("index.html")

# User stuff
@user.route('/users/<username>')
@login_required
def show_user(username):
    return render_template('profile.html', user=username)

@user.route('/signup', methods=['GET', 'POST'])
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
                return redirect(url_for('user.show_user', username=username))
        else:
            flash('passowrds do not match')
        
        return redirect(url_for('user.add_user'))

@user.route('/users/<username>/delete')
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    
    flash('Success! Your user has been deleted.')
    return render_template('success.html')

# Sign in and sign out
@user.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('user.show_user', username=username))
        else:
            flash('wrong username or password')
            return redirect(url_for('user.signin'))

@user.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('user.index'))

# Forms stuff