import streamlit as st

from translations.languages import t


class LoginForm:

    @staticmethod
    def render():

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form("login_form"):

            st.subheader(
                f"🔐 {t('login', language)}"
            )

            email = st.text_input(
                t("email", language)
            )

            password = st.text_input(
                t("password", language),
                type="password"
            )

            submitted = st.form_submit_button(
                t("login", language),
                use_container_width=True
            )

        return (
            email,
            password,
            submitted
        )