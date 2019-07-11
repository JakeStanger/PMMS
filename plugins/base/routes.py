import logging

import helpers
import plugin_loader
from flask import request, Response, jsonify
from flask_login import LoginManager, login_user, login_required, current_user
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

import server
from .tables import User

logger = logging.getLogger(__name__)

logger.debug('Base module routes loading')

login_manager = LoginManager()
login_manager.init_app(server.app)

users = plugin_loader.create_blueprint('users', '/users', 'plugins.base')


@login_manager.user_loader
def load_user_from_username(username: str):
    user = db.session.query(User).filter(db.and_(User.username == username, User.is_deleted == False)).first()
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

    user = load_user_from_username(username)

    if user:
        if check_password_hash(user.password, password):
            login_user(user, True)
            return jsonify({'username': user.username, 'api_key': user.api_key}), 202
        else:
            return Response('{"message": "Invalid password"}', status=401)
    else:
        return Response('{"message": "Invalid username"}', status=401)


@users.route('/signup', methods=['POST'])
def create_user():
    credentials = request.json or request.form
    username = credentials['username']
    password = credentials['password']

    user_exists = load_user_from_username(username) is not None
    if user_exists:
        return Response('{"message": "User already exists"}', status=400)

    user = User(username=username, password=generate_password_hash(password), api_key=helpers.generate_secret_key())
    db.session.add(user)
    db.session.commit()

    login_user(user, True)

    return Response('{"message": "User created"}', status=201)


@users.route('/secure')
@login_required
def secure():
    return current_user.username