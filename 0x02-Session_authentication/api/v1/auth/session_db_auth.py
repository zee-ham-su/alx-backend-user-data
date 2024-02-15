#!/usr/bin/env python3
"""session db auth module
"""
from datetime import datetime, timedelta
from flask import request
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class """
    def create_session(self, user_id=None) -> str:
        """Creates a session id for the user."""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if not sessions:
            return None

        current_time = datetime.now()
        session_lifetime = timedelta(seconds=self.session_duration)
        expiration_time = sessions[0].created_at + session_lifetime

        if expiration_time < current_time:
            return None

        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session."""
        session_id = self.session_cookie(request)

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if not sessions:
            return False

        sessions[0].remove()
        return True
