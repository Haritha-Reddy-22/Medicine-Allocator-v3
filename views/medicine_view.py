
import streamlit as st

from components.forms.medicine_form import MedicineForm
from components.tables.medicine_table import MedicineTable
from core.database import SessionLocal
from core.session import SessionManager
from services.medicine_service import MedicineService
from translations.languages import t


def show_medicines():

    language = st.session_state.get(
        "language",
        "English"
    )

    SessionManager.require_login()
    is_admin = SessionManager.is_admin()

    if is_admin:

        st.title(
            f"💊 {t('medicine_management', language)}"
        )

        st.caption(
            t("manage_medicines", language)
        )

    else:

        st.title(
            f"💊 {t('medicines', language)}"
        )

        st.caption(
            t("search_view_medicines", language)
        )

    # ==========================================
    # ADMIN - ADD MEDICINE
    # ==========================================

    if is_admin:

        st.subheader(
            f"➕ {t('add_medicine', language)}"
        )

        (
            medicine_name,
            generic_name,
            category,
            manufacturer,
            batch_number,
            expiry_date,
            unit_price,
            description,
            prescription_required,
            submitted
        ) = MedicineForm.render()

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
                    description=description,
                    prescription_required=prescription_required
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

    st.subheader(
        f"📋 {t('available_medicines', language)}"
    )

    search = st.text_input(
        f"🔍 {t('search_medicine', language)}",
        placeholder=t(
            "search_medicine_placeholder",
            language
        )
    )

    db = SessionLocal()

    try:

        if search.strip():

            medicines = MedicineService.search_medicines(
                db,
                search
            )

        else:

            medicines = MedicineService.get_all_medicines(
                db
            )

        MedicineTable.render(
            db,
            medicines
        )

    finally:

        db.close()
