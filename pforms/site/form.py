from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_manager, login_required, login_user, logout_user
from pforms.models import User

form = Blueprint('form', __name__)

@form.route('/forms/creation', methods=['GET', 'POST'])
@login_required
def add_form():
    if request.method == 'GET':
        return render_template('formCreation.html')
    else:
        title = resquest.form.get('title')
        description = request.form.description('derscription')

        return render_template('formCreation.html')