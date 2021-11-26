from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user, current_user
from pforms.models import User

user = Blueprint('user', __name__)

# Login manager loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# User stuff
@user.route('/users/home')
def show_user():
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('profile.html', user=username)
    else:
        return redirect(url_for('navigation.index'))

@user.route('/signup', methods=['GET', 'POST'])
def add_user():
    if current_user.is_authenticated:
        flash("Error: you are already signed up")
        return render_template('signup.html')
        
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password2')

        if password_check == password:
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('username or email already in use')
            else:
                user = User(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect(url_for('user.show_user'))
        else:
            flash('passowrds do not match')
        
        return redirect(url_for('user.add_user'))

@user.route('/users/users/delete')
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    
    flash('Success! Your user has been deleted.')
    return render_template('success.html')

# Sign in and sign out
@user.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash("Error: you are already signed in")
        return render_template('signin.html')

    if request.method == 'GET':
        return render_template('signin.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('user.show_user'))
        else:
            flash('wrong username or password')
            return redirect(url_for('user.signin'))

@user.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('navigation.index'))