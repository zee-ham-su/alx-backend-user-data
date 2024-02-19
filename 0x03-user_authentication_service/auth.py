#!/usr/bin/env python3
""" hash_password function
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash_password function
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())