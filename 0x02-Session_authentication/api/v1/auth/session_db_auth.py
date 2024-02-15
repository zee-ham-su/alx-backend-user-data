#!/usr/bin/env python3
"""session db auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None):
        """ create a session for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ return a user_id based on a session_id"""
        if session_id:
            user_session = UserSession.query.filter_by(
                session_id=session_id).first()
            if user_session:
                if self.session_duration <= 0:
                    return user_session.user_id
                elif 'created_at' in user_session and \
                     datetime.strptime(
                         user_session.created_at, "%Y-%m-%d %H:%M:%S") + \
                     timedelta(seconds=self.session_duration) > datetime.now():
                    return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """ delete the user session"""
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.query.filter_by(
                session_id=session_id).first()
            if user_session:
                user_session.delete()
                return True
        return False
