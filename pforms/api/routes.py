from flask import Blueprint, redirect, url_for, request, jsonify

from pforms.extensions import db
from pforms.models import User

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user)


@api.route('/user', methods=['POST'])
def add_user():
    name = request.json.get('username')
    mail = request.json.get('email')

    user = User(username=name, email=mail)
    db.session.add(user)
    db.session.commit()

    return jsonify(user)