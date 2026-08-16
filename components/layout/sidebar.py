import streamlit as st

from core.session import SessionManager


class Sidebar:

    @staticmethod
    def render():

        with st.sidebar:

            st.markdown(
                """
                <div style="text-align:center;">
                    <h1>🏥</h1>
                    <h2 style="margin-bottom:0;">
                        Medicine Allocator Pro
                    </h2>
                    <p style="color:#64748B;">
                        Healthcare Management System
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            if SessionManager.is_logged_in():

                user = SessionManager.get_user()

                st.success(
                    f"👤 {user['name']}"
                )

                st.caption(
                    f"Role: {user['role']}"
                )

            st.divider()

            st.markdown("### 📋 Navigation")

            st.info(
                "Use the page menu above to navigate through the application."
            )

            st.divider()

            st.markdown("### ℹ️ System Status")

            st.success("🟢 System Online")

            st.caption("Version 1.0")