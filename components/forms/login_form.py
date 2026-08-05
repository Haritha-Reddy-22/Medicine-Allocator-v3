import streamlit as st


class LoginForm:

    @staticmethod
    def render():

        with st.form("login_form"):

            st.subheader("🔐 Login")

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        return (
            email,
            password,
            submitted
        )