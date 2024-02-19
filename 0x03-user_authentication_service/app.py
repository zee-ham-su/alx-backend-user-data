#!/usr/bin/env python3
""" basic flask app"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
