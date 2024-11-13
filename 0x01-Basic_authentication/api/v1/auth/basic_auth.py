#!/usr/bin/env python3
'''
A class to manage API authentication
'''
import base64
from flask import request
from typing import (List, TypeVar, Dict)
from api.v1.auth.auth import Auth
from models import base
from models.user import User


class BasicAuth(Auth):
    '''
    A class to manage API authentication
    '''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        value = authorization_header.split(" ")[1]
        return value

    def decode_base64_authorization_header(self,
                                           base64_auth_header: str) -> str:
        """ Returns the decoded value of Base64 string
        """
        if base64_auth_header is None:
            return None
        if type(base64_auth_header) is not str:
            return None
        try:
            headerBytes = bytes(base64_auth_header, 'utf-8')
            decodedHeader = base64.decodestring(headerBytes)
            return decodedHeader.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_b64_auth_header: str) -> (str, str):
        """ Returns the Email and Password from the Base64 decoded value
        """
        if decoded_b64_auth_header is None:
            return (None, None)
        if type(decoded_b64_auth_header) is not str:
            return (None, None)
        if ":" not in decoded_b64_auth_header:
            return (None, None)
        email, password = decoded_b64_auth_header.split(":")
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        allUsers: Dict = base.DATA.get('User')
        if not allUsers:
            return None
        userByEmail: List = User.search({'email': user_email})
        if not userByEmail:
            return None
        user = userByEmail[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a Flask request Object
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        auth_header = self.decode_base64_authorization_header(b64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(auth_header)
        userObj = self.user_object_from_credentials(user_email, user_pwd)
        if userObj is None:
            return None
        return userObj
