import streamlit as st

from core.session import SessionManager

st.title("🏠 Dashboard")

if not SessionManager.is_logged_in():

    st.error("Please login first.")

    st.stop()

user = SessionManager.get_user()

st.success("✅ Login Successful")

st.write(f"Welcome **{user['name']}**")

st.write("Email :", user["email"])

st.write("Role :", user["role"])

if st.button("Logout"):

    SessionManager.logout()

    st.success("Logged out successfully.")

    st.rerun()