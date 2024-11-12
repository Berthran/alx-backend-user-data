#!/usr/bin/env python3
'''
A class to manage API authentication
'''
import base64
from flask import request
from typing import (List, TypeVar)
from api.v1.auth.auth import Auth


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
