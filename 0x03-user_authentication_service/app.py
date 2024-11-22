#!/usr/bin/env python3
"""
Basic Flask App
"""


from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy.orm.exc import NoResultFound


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    '''Home route
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    '''Register user route
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify({'email': email, 'message': "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Login registerd users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = make_response()
        response.set_cookie("session_id", session_id)
        return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
