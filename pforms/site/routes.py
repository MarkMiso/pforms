from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user
from pforms.models import User

site = Blueprint('site', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/users/<username>')
@login_required
def show_user(username):
    return render_template('profile.html', user=username)

@site.route('/users/<username>/delete')
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()

    return render_template('success.html')

@site.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('user')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('site.show_user', username=username))
        else:
            flash('wrong username or password')
            return redirect(url_for('site.login'))

@site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.index'))

@site.route('/signup', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password2')

        if username and email and password and password_check:
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
        else:
            flash('all fields are required')
         
        return redirect(url_for('site.add_user'))