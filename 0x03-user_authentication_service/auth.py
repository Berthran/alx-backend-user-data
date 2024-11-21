#!/usr/bin/env python3
'''
Hash user password
'''

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        '''Constructor function
        '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user with email and password
        """
        try:
            userExits = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound as e:
            hashedpwd = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashedpwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a login
        """
        try:
            user = self._db.find_user_by(email=email)
            bytespassword = password.encode('utf-8')
            passwordIsCorrect = bcrypt.checkpw(bytespassword,
                                               user.hashed_password)
            if passwordIsCorrect:
                return True
            return False
        except NoResultFound:
            return False

    @property
    def _generate_uuid(self) -> str:
        """Returns string representation of a uuid
        """
        return str(uuid.uuid4())
