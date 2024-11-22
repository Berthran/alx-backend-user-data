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


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Get's token for password reset
    """
    email = request.form.get("email")
    session_id = AUTH.create_session(email)
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        reset_token = AUTH.get_reset_password_token(user.email)
        return jsonify({
                            "email": email,
                            "reset_token": reset_token
                       }), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Changes user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
