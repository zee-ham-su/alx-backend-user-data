#!/usr/bin/env python3
""" Session authentication module
"""
from models.user import User
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session"""
        if request is None:
            return False

        session_cookie_id = self.session_cookie(request)
        if not session_cookie_id:
            return False

        user_id = self.user_id_for_session_id(session_cookie_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_cookie_id]
        return True
