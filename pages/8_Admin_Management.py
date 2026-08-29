
import streamlit as st

from core.database import SessionLocal
from core.session import SessionManager
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from utils.permissions import Permissions


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)


# ==========================================
# ACCESS CONTROL
# ==========================================

Permissions.require_admin()


# ==========================================
# PAGE HEADER
# ==========================================

st.title("👥 User Management")

st.write(
    "View users and manage their roles and account status."
)

st.divider()


# ==========================================
# DATABASE
# ==========================================

db = SessionLocal()


try:

    # ======================================
    # CURRENT ADMIN
    # ======================================

    current_admin_id = SessionManager.get_user_id()

    # ======================================
    # GET ALL USERS
    # ======================================

    users = UserRepository.get_all_users(db)

    # ======================================
    # COUNT ADMINS
    # ======================================

    admin_count = UserRepository.count_admins(db)

    # ======================================
    # SUMMARY
    # ======================================

    total_users = len(users)

    normal_users = sum(
        1
        for user in users
        if str(user.role).upper() == "USER"
    )

    admins = sum(
        1
        for user in users
        if str(user.role).upper() == "ADMIN"
    )

    # ======================================
    # METRICS
    # ======================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👥 Total Users",
            total_users
        )

    with col2:

        st.metric(
            "👤 Users",
            normal_users
        )

    with col3:

        st.metric(
            "👑 Administrators",
            admins
        )

    st.divider()

    # ======================================
    # SEARCH AND FILTER
    # ======================================

    col1, col2 = st.columns([2, 1])

    with col1:

        search = st.text_input(
            "🔍 Search users",
            placeholder="Search by name, email, or phone..."
        ).strip().lower()

    with col2:

        filter_role = st.selectbox(
            "Filter by role",
            [
                "ALL",
                "USER",
                "ADMIN"
            ]
        )

    # ======================================
    # FILTER USERS
    # ======================================

    filtered_users = []

    for user in users:

        role = str(user.role).upper()

        # Role filter
        if (
            filter_role != "ALL"
            and role != filter_role
        ):
            continue

        # Search filter
        if search:

            searchable_text = " ".join(
                [
                    str(user.full_name or ""),
                    str(user.email or ""),
                    str(user.phone or "")
                ]
            ).lower()

            if search not in searchable_text:
                continue

        filtered_users.append(user)

    # ======================================
    # RESULT COUNT
    # ======================================

    st.write(
        f"Showing **{len(filtered_users)}** user(s)"
    )

    st.divider()

    # ======================================
    # NO USERS
    # ======================================

    if not filtered_users:

        st.info(
            "No users found matching your search."
        )

    # ======================================
    # USER LIST
    # ======================================

    else:

        for user in filtered_users:

            role = str(user.role).upper()

            is_current_admin = (
                user.id == current_admin_id
                and role == "ADMIN"
            )

            with st.container(border=True):

                # ==================================
                # USER INFORMATION
                # ==================================

                col1, col2, col3, col4 = st.columns(
                    [2.7, 2, 1, 1.5]
                )

                # ----------------------------------
                # NAME / CONTACT
                # ----------------------------------

                with col1:

                    st.markdown(
                        f"### {user.full_name}"
                    )

                    st.caption(
                        f"📧 {user.email}"
                    )

                    st.caption(
                        f"📱 {user.phone}"
                    )

                # ----------------------------------
                # ROLE / STATUS
                # ----------------------------------

                with col2:

                    if role == "ADMIN":

                        st.success(
                            "👑 ADMIN"
                        )

                    else:

                        st.info(
                            "👤 USER"
                        )

                    if user.is_active:

                        st.caption(
                            "🟢 Active"
                        )

                    else:

                        st.caption(
                            "🔴 Inactive"
                        )

                # ----------------------------------
                # USER ID
                # ----------------------------------

                with col3:

                    st.caption(
                        f"ID: {user.id}"
                    )

                # ----------------------------------
                # ACTION
                # ----------------------------------

                with col4:

                    # ==============================
                    # USER → ADMIN
                    # ==============================

                    if role == "USER":

                        if st.button(
                            "⬆️ Promote",
                            key=f"promote_{user.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                AuthService.update_user_role(
                                    db=db,
                                    user_id=user.id,
                                    role="ADMIN",
                                    current_admin_id=current_admin_id
                                )
                            )

                            if success:

                                st.success(message)

                                st.rerun()

                            else:

                                st.error(message)

                    # ==============================
                    # ADMIN → USER
                    # ==============================

                    else:

                        # --------------------------------
                        # Current logged-in admin
                        # --------------------------------

                        if is_current_admin:

                            st.button(
                                "🔒 Your Account",
                                key=f"self_{user.id}",
                                disabled=True,
                                use_container_width=True
                            )

                            st.caption(
                                "Cannot demote yourself"
                            )

                        # --------------------------------
                        # Last ADMIN
                        # --------------------------------

                        elif admin_count <= 1:

                            st.button(
                                "🔒 Demote",
                                key=f"demote_{user.id}",
                                disabled=True,
                                use_container_width=True
                            )

                            st.caption(
                                "Last ADMIN"
                            )

                        # --------------------------------
                        # Normal ADMIN
                        # --------------------------------

                        else:

                            if st.button(
                                "⬇️ Demote",
                                key=f"demote_{user.id}",
                                use_container_width=True
                            ):

                                success, message = (
                                    AuthService.update_user_role(
                                        db=db,
                                        user_id=user.id,
                                        role="USER",
                                        current_admin_id=current_admin_id
                                    )
                                )

                                if success:

                                    st.success(message)

                                    st.rerun()

                                else:

                                    st.error(message)


finally:

    db.close()

