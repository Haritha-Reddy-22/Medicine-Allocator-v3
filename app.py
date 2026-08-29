
import streamlit as st

from config.settings import APP_NAME, DATABASE_PATH
from core.database import initialize_database
from core.session import SessionManager


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

print("Database Path:", DATABASE_PATH)

initialize_database()


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💊",
    layout="wide"
)


# ==========================================
# PAGE DEFINITIONS
# ==========================================

login_page = st.Page(
    "pages/0_Login.py",
    title="Login",
    icon="🔐"
)

signup_page = st.Page(
    "pages/1_Signup.py",
    title="Signup",
    icon="📝"
)

dashboard_page = st.Page(
    "pages/2_Dashboard.py",
    title="Dashboard",
    icon="🏠"
)

hospitals_page = st.Page(
    "pages/3_Hospitals.py",
    title="Hospitals",
    icon="🏥"
)

medicines_page = st.Page(
    "pages/4_Medicines.py",
    title="Medicines",
    icon="💊"
)

inventory_page = st.Page(
    "pages/5_Inventory.py",
    title="Inventory",
    icon="📦"
)

medicine_allocator_page = st.Page(
    "pages/6_Medicine_Allocator.py",
    title="Medicine Allocator",
    icon="📍"
)

reservations_page = st.Page(
    "pages/6_Reservations.py",
    title="Reservations",
    icon="📋"
)

reports_page = st.Page(
    "pages/7_Reports.py",
    title="Reports",
    icon="📊"
)

admin_management_page = st.Page(
    "pages/8_Admin_Management.py",
    title="Admin Management",
    icon="👑"
)

user_management_page = st.Page(
    "pages/8_User_Management.py",
    title="User Management",
    icon="👥"
)


# ==========================================
# LOGIN STATUS
# ==========================================

logged_in = SessionManager.is_logged_in()


# ==========================================
# LOGGED OUT NAVIGATION
# ==========================================

if not logged_in:

    navigation = st.navigation(
        [
            login_page,
            signup_page
        ]
    )

    navigation.run()


# ==========================================
# LOGGED IN NAVIGATION
# ==========================================

else:

    role = SessionManager.get_role()

    # ======================================
    # USER PAGES
    # ======================================

    user_pages = [
        dashboard_page,
        hospitals_page,
        medicines_page,
        medicine_allocator_page,
        reservations_page
    ]

    # ======================================
    # ADMIN PAGES
    # ======================================

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

    # ======================================
    # ADMIN NAVIGATION
    # ======================================

    if role == "ADMIN":

        navigation = st.navigation(
            admin_pages
        )

    # ======================================
    # USER NAVIGATION
    # ======================================

    else:

        navigation = st.navigation(
            user_pages
        )

    navigation.run()

