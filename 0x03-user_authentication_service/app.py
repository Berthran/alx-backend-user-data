#!/usr/bin/env python
"""
Basic Flask App
"""


from flask import Flask, jsonify, request
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    '''Home route
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''Register user route
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify({'email': email, 'message': "user_created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
