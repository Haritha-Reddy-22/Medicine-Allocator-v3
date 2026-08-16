import streamlit as st


class SignupForm:

    @staticmethod
    def render():

        with st.form("signup_form"):

            st.subheader("📝 Create Account")

            full_name = st.text_input(
                "Full Name"
            )

            email = st.text_input(
                "Email"
            )

            phone = st.text_input(
                "Phone Number"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Create Account",
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