import streamlit as st

from components.forms.signup_form import SignupForm
from services.auth_service import AuthService
from core.database import SessionLocal


def show_signup():

    st.title("📝 Create Account")

    (
        full_name,
        email,
        phone,
        password,
        confirm_password,
        submitted
    ) = SignupForm.render()

    if submitted:

        if not full_name.strip():

            st.warning(
                "Please enter your full name."
            )

            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        db = SessionLocal()

        try:

            success, result = AuthService.register_user(
                db=db,
                full_name=full_name,
                email=email,
                phone=phone,
                password=password
            )

            if success:

                st.success(
                    "✅ Account Created Successfully!"
                )

            else:

                st.error(result)

        except Exception as e:

            st.exception(e)

        finally:

            db.close()