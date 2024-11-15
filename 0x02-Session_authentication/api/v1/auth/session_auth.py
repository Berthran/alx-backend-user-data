#!/usr/bin/env python3
'''
A class to manage API authentication
'''
import re
from flask import request
from typing import (List, TypeVar)
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''
    A class to manage API authentication
    '''
