import streamlit as st


class SessionManager:

    @staticmethod
    def login(user):

        st.session_state["logged_in"] = True

        st.session_state["user"] = {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role
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