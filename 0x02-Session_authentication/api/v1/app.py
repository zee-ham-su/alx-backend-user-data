#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()


@app.before_request
def before_request():
    """ to filter each request
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        filtered_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/',
                         '/api/v1/forbidden/',
                         '/api/v1/auth_session/login/']

        if auth.require_auth(request.path, filtered_list):
            if auth.authorization_header(
                    request) is None and auth.session_cookie(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
