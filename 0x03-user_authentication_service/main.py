#!/usr/bin/env python3
'''
End-to-end integration testing
'''


import requests


def register_user(email: str, password: str) -> None:
    '''Register a user
    @app.route('/users', methods=['POST'])
    '''
    url = "http://localhost:5000/users"
    data = {
            'email': email,
            'password': password
            }
    response = requests.post(url, data=data)
    assert response.status_code == 200

    expected_response = {'email': email, 'message': "user created"}
    response_json = response.json()
    assert response_json == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    '''Login with wrong password
    @app.route('/sessions', methods=['POST'])
    '''
    url = "http://localhost:5000/sessions"
    data = {
            'email': email,
            'password': password
            }
    response = requests.post(url, data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Login wiht correct credentials
    @app.route('/sessions', methods=['POST'])
    expected_response = {
                            "email": email,
                            "message": "logged in"
                        }
    '''
    url = "http://localhost:5000/sessions"
    data = {
            'email': email,
            'password': password
            }
    response = requests.post(url, data)
    assert response.status_code == 200

    expected_response = {'email': email, 'message': "logged in"}
    response_json = response.json()
    assert response_json == expected_response


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    log_in(EMAIL, PASSWD)
