import streamlit as st

from core.session import SessionManager


class Permissions:

    @staticmethod
    def is_admin():

        user = SessionManager.get_user()

        if not user:
            return False

        return user.get("role", "").upper() == "ADMIN"

    @staticmethod
    def is_user():

        user = SessionManager.get_user()

        if not user:
            return False

        return user.get("role", "").upper() == "USER"

    @staticmethod
    def require_login():

        if not SessionManager.is_logged_in():

            st.error("Please login first.")
            st.stop()

    @staticmethod
    def require_admin():

        Permissions.require_login()

        if not Permissions.is_admin():

            st.error(
                "🚫 Access denied. "
                "Administrator privileges are required."
            )

            st.stop()