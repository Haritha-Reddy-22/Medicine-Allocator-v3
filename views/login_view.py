import streamlit as st

from components.forms.login_form import LoginForm
from services.auth_service import AuthService
from core.database import SessionLocal
from core.session import SessionManager


def show_login():

    st.title("🔐 Login")

    email, password, submitted = LoginForm.render()

    if submitted:

        if not email.strip() or not password.strip():
            st.warning("Please enter Email and Password.")
            return

        db = SessionLocal()

        try:

            success, result = AuthService.login_user(
                db=db,
                email=email,
                password=password
            )

            if success:

                # Save user in session
                SessionManager.login(result)

                # Show success message
                st.success("✅ Login Successful!")

                st.info("👉 Now click 'Dashboard' from the left sidebar.")

            else:

                st.error(result)

        except Exception as e:

            st.exception(e)

        finally:

            db.close()