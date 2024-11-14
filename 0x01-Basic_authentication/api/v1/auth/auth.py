#!/usr/bin/env python3
'''
A class to manage API authentication
'''
import re
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
        if path is None or excluded_paths is None:
            return True
        path = path if path.endswith('/') else path + '/'
        for pathExp in excluded_paths:
            pattern = rf"{pathExp}"
            if re.fullmatch(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns a header for authorization
        """
        if request is None:
            return None
        if "Authorization" in request.headers:
            value = request.headers['Authorization']
            return value
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a Flask request Object
        """
        return None
