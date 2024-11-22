#!/usr/bin/env python3
"""
Basic Flask App
"""


from auth import Auth
from flask import Flask, jsonify, request, abort, make_response, redirect
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
        response = make_response(jsonify({
                                            "email": email,
                                            "message": "logged in"
                                        }))
        response.set_cookie("session_id", session_id, httponly=True)
        return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logouts user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """User profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
