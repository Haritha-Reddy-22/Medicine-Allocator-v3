import streamlit as st

from translations.languages import t


class SignupForm:

    @staticmethod
    def render():

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form("signup_form"):

            st.subheader(
                f"📝 {t('signup', language)}"
            )

            full_name = st.text_input(
                t("full_name", language)
            )

            email = st.text_input(
                t("email", language)
            )

            phone = st.text_input(
                t("phone_number", language)
            )

            password = st.text_input(
                t("password", language),
                type="password"
            )

            confirm_password = st.text_input(
                t("confirm_password", language),
                type="password"
            )

            submitted = st.form_submit_button(
                t("signup", language),
                use_container_width=True
            )

        return (
            full_name,
            email,
            phone,
            password,
            confirm_password,
            submitted
        )