#!/usr/bin/python3 env
'''
Hash user password
'''

import bcrypt


def _hash_password(password: str) -> bytes:
    ''' Hashes a user's password
    '''
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
