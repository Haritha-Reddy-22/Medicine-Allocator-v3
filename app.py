import streamlit as st

from config.settings import APP_NAME, DATABASE_PATH
from core.database import initialize_database

print("Database Path:", DATABASE_PATH)

initialize_database()

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💊",
    layout="wide"
)

st.title("💊 Medicine Allocator")

st.success("Database Connected Successfully ✅")