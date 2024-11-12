#!/usr/bin/env python3
'''
A class to manage API authentication
'''
from flask import request
from typing import (List, TypeVar)


class Auth:
    '''
    A class to manage API authentication
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a API endpoint requires authentication
        Returns:
            - False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns a header for authorization
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a Flask request Object
        """
        return None
