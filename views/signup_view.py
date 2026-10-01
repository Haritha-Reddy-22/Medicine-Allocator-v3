import streamlit as st

from components.forms.signup_form import SignupForm
from services.auth_service import AuthService
from core.database import SessionLocal
from translations.languages import t


def show_signup():

    language = st.session_state.get(
        "language",
        "English"
    )

    st.title(
        f"📝 {t('signup', language)}"
    )

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
                f"⚠️ {t('warning', language)}: "
                "Please enter your full name."
            )

            return

        if password != confirm_password:

            st.error(
                "❌ Passwords do not match."
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
                    f"✅ {t('success', language)}! "
                    "Account Created Successfully!"
                )

            else:

                st.error(result)

        except Exception as e:

            st.exception(e)

        finally:

            db.close()