import logging
from typing import Union

import helpers
import plugin_loader
from flask import request, jsonify, redirect
from flask_login import LoginManager, login_user, logout_user
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

import server
from .models import User

logger = logging.getLogger(__name__)

logger.debug('Base module routes loading')

login_manager = LoginManager()
login_manager.init_app(server.app)

users = plugin_loader.create_blueprint('users', '/users', 'plugins.base')


@login_manager.user_loader
def load_user_from_username_or_id(username: Union[str, int]):
    if not username.isdigit():
        user = db.session.query(User).filter(db.and_(User.username == username, User.is_deleted == False)).first()
    else:
        user = db.session.query(User).filter(db.and_(User.id == username, User.is_deleted == False)).first()
    return user


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key') or request.headers.get('Authorization')

    if api_key:
        user = db.session.query(User).filter(db.and_(User.api_key == api_key, User.is_deleted == False)).first()
        if user:
            return user


@server.app.errorhandler(401)
def unauthorized(e):
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'message': str(e)}), 401


@users.route('/login', methods=['POST'])
def login():
    """
    Logs in a user using cookies for browser storage
    :return: JSON containing username and API key
    """
    credentials = request.json or request.form
    username = credentials['username']
    password = credentials['password']

    user = load_user_from_username_or_id(username)

    if user:
        if check_password_hash(user.password, password):
            login_user(user, True)

            if 'text/html' in request.accept_mimetypes:
                next = request.args.get('next')
                return redirect(next or '/')

            return jsonify({'username': user.username, 'api_key': user.api_key}), 202
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'Invalid username'}), 401


@users.route('/signup', methods=['POST'])
def create_user():
    credentials = request.json or request.form
    username = credentials['username']
    password = credentials['password']

    user_exists = load_user_from_username_or_id(username) is not None
    if user_exists:
        return jsonify({'message': 'User already exists'}), 400

    user = User(username=username, password=generate_password_hash(password), api_key=helpers.generate_secret_key())
    db.session.add(user)
    db.session.commit()

    login_user(user, True)

    return jsonify({'message': 'User created'}), 201


@users.route('/logout')
def logout():
    logout_user()

    if 'text/html' in request.accept_mimetypes:
        return redirect('/')

    return jsonify({'message': 'Logged out'}), 200
