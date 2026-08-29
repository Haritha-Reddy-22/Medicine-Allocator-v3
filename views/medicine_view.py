
import streamlit as st

from components.forms.medicine_form import MedicineForm
from components.tables.medicine_table import MedicineTable
from core.database import SessionLocal
from core.session import SessionManager
from services.medicine_service import MedicineService


def show_medicines():

    # ==========================================
    # LOGIN REQUIRED
    # ==========================================

    SessionManager.require_login()

    # ==========================================
    # GET CURRENT USER ROLE
    # ==========================================

    is_admin = SessionManager.is_admin()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    if is_admin:

        st.title("💊 Medicine Management")

        st.caption(
            "Manage and view medicines in the system."
        )

    else:

        st.title("💊 Medicines")

        st.caption(
            "Search and view available medicines."
        )

    # ==========================================
    # ADMIN: ADD MEDICINE
    # ==========================================

    if is_admin:

        st.subheader("➕ Add Medicine")

        (
            medicine_name,
            generic_name,
            category,
            manufacturer,
            batch_number,
            expiry_date,
            unit_price,
            description,
            submitted
        ) = MedicineForm.render()

        # ======================================
        # ADD MEDICINE
        # ======================================

        if submitted:

            db = SessionLocal()

            try:

                success, message = MedicineService.add_medicine(
                    db=db,
                    medicine_name=medicine_name,
                    generic_name=generic_name,
                    category=category,
                    manufacturer=manufacturer,
                    batch_number=batch_number,
                    expiry_date=expiry_date,
                    unit_price=unit_price,
                    description=description
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

            finally:

                db.close()

        st.divider()

    # ==========================================
    # MEDICINE LIST
    # ==========================================

    st.subheader("📋 Available Medicines")

    # ==========================================
    # SEARCH
    # ==========================================

    search = st.text_input(
        "🔍 Search Medicine",
        placeholder=(
            "Search by medicine name, "
            "generic name or category"
        )
    )

    # ==========================================
    # DATABASE
    # ==========================================

    db = SessionLocal()

    try:

        # ======================================
        # SEARCH MEDICINES
        # ======================================

        if search.strip():

            medicines = MedicineService.search_medicines(
                db,
                search
            )

        else:

            medicines = MedicineService.get_all_medicines(
                db
            )

        # ======================================
        # DISPLAY MEDICINES
        # ======================================

        MedicineTable.render(
            db,
            medicines
        )

    finally:

        db.close()

