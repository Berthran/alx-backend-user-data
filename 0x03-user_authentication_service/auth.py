#!/usr/bin/env python3
'''
Hash user password
'''

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    ''' Hashes a user's password
    '''
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: bytes) -> User:
        """Registers a user with email and password
        """
