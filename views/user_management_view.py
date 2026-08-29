import streamlit as st

from core.database import SessionLocal
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from utils.permissions import Permissions


def show_user_management():

    # ==========================================
    # ADMIN ACCESS
    # ==========================================

    Permissions.require_admin()

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("👥 User Management")

    st.write(
        "Manage user accounts and administrator permissions."
    )

    st.divider()

    db = SessionLocal()

    try:

        users = UserRepository.get_all_users(db)

        if not users:

            st.info("No users found.")
            return

        # ==========================================
        # USER LIST
        # ==========================================

        for user in users:

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [5, 2, 2]
                )

                with col1:

                    st.markdown(
                        f"""
### 👤 {user.full_name}

📧 **Email:** {user.email}

📱 **Phone:** {user.phone}

📌 **Current Role:** {user.role}
"""
                    )

                with col2:

                    if user.role == "ADMIN":

                        st.success("👑 ADMIN")

                    else:

                        st.info("👤 USER")

                with col3:

                    # ----------------------------------
                    # DO NOT ALLOW ADMIN TO DEMOTE SELF
                    # ----------------------------------

                    current_user = (
                        st.session_state.get(
                            "user",
                            {}
                        )
                    )

                    current_user_id = current_user.get(
                        "id"
                    )

                    if user.id == current_user_id:

                        st.caption(
                            "Current account"
                        )

                    elif user.role == "USER":

                        if st.button(
                            "⬆️ Make Admin",
                            key=f"promote_{user.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                AuthService.update_user_role(
                                    db,
                                    user.id,
                                    "ADMIN"
                                )
                            )

                            if success:

                                st.success(message)
                                st.rerun()

                            else:

                                st.error(message)

                    else:

                        if st.button(
                            "⬇️ Make User",
                            key=f"demote_{user.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                AuthService.update_user_role(
                                    db,
                                    user.id,
                                    "USER"
                                )
                            )

                            if success:

                                st.success(message)
                                st.rerun()

                            else:

                                st.error(message)

    finally:

        db.close()