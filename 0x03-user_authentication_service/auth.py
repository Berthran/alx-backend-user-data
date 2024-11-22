#!/usr/bin/env python3
'''
Hash user password
'''

import uuid
import bcrypt
from db import DB
from user import User
from flask import session
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    ''' Hashes a user's password
    '''
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """Returns string representation of a uuid
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> session:
        """Creats a session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets a user from a session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Removes the user.session_id attribute
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Gets a reset token
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            return reset_token
        except NoResultFound:
            raise ValueError()
