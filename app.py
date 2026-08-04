import streamlit as st

from config.settings import APP_NAME
from core.database import initialize_database

# Create database
initialize_database()

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💊",
    layout="wide"
)

st.title("💊 Medicine Allocator")

st.success("Database Connected Successfully ✅")