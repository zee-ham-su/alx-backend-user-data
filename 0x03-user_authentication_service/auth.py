#!/usr/bin/env python3
""" hash_password function
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ hash_password function
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generate_uuid function
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register_user method
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass
        hashed_pwd = _hash_password(password)
        new_user = self._db.add_user(email, hashed_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for a user.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Getting user corresponding with a session ID.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session.
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
        return None
