#!/usr/bin/env python3
""" basic flask app"""
from flask import (Flask, jsonify,
                   request, abort, make_response,
                   redirect)
from auth import Auth

app = Flask(__name__)
strict_slashes = False
AUTH = Auth()


@app.route("/")
def main():
    """ main route"""
    data = {
        "message": "Bienvenue"
    }
    return jsonify(data)


@app.route("/users", methods=["POST"])
def register_user():
    """ register a user with email and password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        response = {
            "email": new_user.email,
            "message": "user created"
        }
        return jsonify(response), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """ login route
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email,
                     "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """  route for logging out
    """
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """ profile route
    """
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    response = {
        "email": user.email
    }
    return jsonify(response), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ get reset password token
    """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        response = {
            "email": email,
            "reset_token": token
        }
        return jsonify(response)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
