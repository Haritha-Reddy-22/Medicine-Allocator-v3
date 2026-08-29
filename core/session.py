import streamlit as st


class SessionManager:

    @staticmethod
    def login(user):

        st.session_state["logged_in"] = True

        st.session_state["user"] = {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": str(user.role).upper()
        }

    @staticmethod
    def logout():

        st.session_state.clear()

    @staticmethod
    def is_logged_in():

        return st.session_state.get(
            "logged_in",
            False
        )

    @staticmethod
    def get_user():

        return st.session_state.get(
            "user",
            None
        )

    @staticmethod
    def get_user_id():

        user = SessionManager.get_user()

        if user:
            return user.get("id")

        return None

    @staticmethod
    def get_user_name():

        user = SessionManager.get_user()

        if user:
            return user.get("name")

        return None

    @staticmethod
    def get_user_email():

        user = SessionManager.get_user()

        if user:
            return user.get("email")

        return None

    @staticmethod
    def get_role():

        user = SessionManager.get_user()

        if user:
            return str(user.get("role", "")).upper()

        return None

    @staticmethod
    def is_admin():

        return SessionManager.get_role() == "ADMIN"

    @staticmethod
    def is_user():

        return SessionManager.get_role() == "USER"

    @staticmethod
    def require_login():

        if not SessionManager.is_logged_in():

            st.error("🔒 Please login to access this page.")

            st.stop()

    @staticmethod
    def require_admin():

        SessionManager.require_login()

        if not SessionManager.is_admin():

            st.error(
                "🚫 Access Denied: "
                "Administrator privileges are required."
            )

            st.stop()

    @staticmethod
    def require_user():

        SessionManager.require_login()

        if not (
            SessionManager.is_user()
            or SessionManager.is_admin()
        ):

            st.error("🚫 Access Denied.")

            st.stop()