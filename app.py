import streamlit as st

from config.settings import APP_NAME, DATABASE_PATH
from core.database import initialize_database
from core.session import SessionManager
from translations.languages import LANGUAGES, t


# ==========================================================
# DATABASE
# ==========================================================

print("Database Path:", DATABASE_PATH)

initialize_database()


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💊",
    layout="wide"
)


# ==========================================================
# LANGUAGE
# ==========================================================

if "language" not in st.session_state:

    st.session_state.language = "English"


selected_language = st.sidebar.selectbox(

    "🌐 Language / భాష / भाषा",

    options=list(LANGUAGES.keys()),

    index=list(LANGUAGES.keys()).index(
        st.session_state.language
    )

)


# Detect language change
if selected_language != st.session_state.language:

    st.session_state.language = selected_language

    st.rerun()


language = st.session_state.language


# ==========================================================
# PAGE DEFINITIONS
# ==========================================================

login_page = st.Page(

    "pages/0_Login.py",

    title=t(
        "login",
        language
    ),

    icon="🔐"
)


signup_page = st.Page(

    "pages/1_Signup.py",

    title=t(
        "signup",
        language
    ),

    icon="📝"
)


dashboard_page = st.Page(

    "pages/2_Dashboard.py",

    title=t(
        "dashboard",
        language
    ),

    icon="🏠"
)


hospitals_page = st.Page(

    "pages/3_Hospitals.py",

    title=t(
        "hospitals",
        language
    ),

    icon="🏥"
)


medicines_page = st.Page(

    "pages/4_Medicines.py",

    title=t(
        "medicines",
        language
    ),

    icon="💊"
)


inventory_page = st.Page(

    "pages/5_Inventory.py",

    title=t(
        "inventory",
        language
    ),

    icon="📦"
)


medicine_allocator_page = st.Page(

    "pages/6_Medicine_Allocator.py",

    title=t(
        "medicine_allocator",
        language
    ),

    icon="📍"
)


reservations_page = st.Page(

    "pages/6_Reservations.py",

    title=t(
        "reservations",
        language
    ),

    icon="📋"
)


reports_page = st.Page(

    "pages/7_Reports.py",

    title=t(
        "reports",
        language
    ),

    icon="📊"
)


admin_management_page = st.Page(

    "pages/8_Admin_Management.py",

    title=t(
        "admin_management",
        language
    ),

    icon="👑"
)


user_management_page = st.Page(

    "pages/8_User_Management.py",

    title=t(
        "user_management",
        language
    ),

    icon="👥"
)


# ==========================================================
# NAVIGATION
# ==========================================================

logged_in = SessionManager.is_logged_in()


if not logged_in:

    navigation = st.navigation(

        [
            login_page,
            signup_page
        ]

    )

else:

    role = SessionManager.get_role()

    user_pages = [

        dashboard_page,

        hospitals_page,

        medicines_page,

        medicine_allocator_page,

        reservations_page

    ]

    admin_pages = [

        dashboard_page,

        hospitals_page,

        medicines_page,

        inventory_page,

        medicine_allocator_page,

        reservations_page,

        reports_page,

        user_management_page

    ]

    if role == "ADMIN":

        navigation = st.navigation(
            admin_pages
        )

    else:

        navigation = st.navigation(
            user_pages
        )


# ==========================================================
# RUN
# ==========================================================

navigation.run()