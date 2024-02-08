#!/usr/bin/env python3
"""Implement a hash_password function
"""

import bcrypt
from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    """Implement a hash_password function
    """
    hashed = password.encode()
    return bcrypt.hashpw(hashed, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement a is_valid function
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
