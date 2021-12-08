from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user, current_user
from pforms.models import User, Form

user = Blueprint('user', __name__)

### Login manager loader ###
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


### USER HOME
# GET:  render user profile or index
###
@user.route('/users/home')
def show_user():
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('profile.html', user=username)
    else:
        return redirect(url_for('navigation.index'))


### SIGN UP
# GET:  render signup form
# POST: add user to database and render profile
###
@user.route('/signup', methods=['GET', 'POST'])
def add_user():
    # prevent signup from already signed in user
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

        # password check
        if password_check == password:
            # unique username and mail check
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('username or email already in use')
            else:
                # add and login user
                user = User(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect(url_for('user.show_user'))
        else:
            flash('passowrds do not match')
        
        return redirect(url_for('user.add_user'))


### USER DELETION
# GET:  deletes current user and all associated forms but keeps forms submissions
###
@user.route('/users/delete')
@login_required
def delete_user():
    current_user.delete()
    db.session.commit()
    logout_user()
    
    flash('Success! Your user has been deleted.')
    return render_template('success.html')


### SIGN IN
# GET:  render signin form
# POST: sign in user and render profile page or render signin form
###
@user.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash("Error: you are already signed in")
        return render_template('signin.html')

    if request.method == 'GET':
        return render_template('signin.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # user existence and password check
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('user.show_user'))
        else:
            flash('wrong email or password')
            return redirect(url_for('user.signin'))


### SIGN OUT
# GET:  signout user and render index
###
@user.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('navigation.index'))