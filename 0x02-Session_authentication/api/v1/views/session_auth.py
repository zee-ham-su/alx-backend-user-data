#!/usr/bin/env python3
"""new Flask view that handles all routes
for the Session authentication
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_session_auth():
    """ POST /auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if user is None or user == []:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.auth.session_auth import SessionAuth
    session = SessionAuth().create_session(user.id)
    data = jsonify(user.to_json())
    data.set_cookie('session_id', session)
    return data
