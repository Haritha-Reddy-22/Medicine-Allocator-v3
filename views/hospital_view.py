import streamlit as st

from components.forms.hospital_form import HospitalForm
from components.tables.hospital_table import HospitalTable
from core.database import SessionLocal
from core.session import SessionManager
from utils.permissions import Permissions
from services.hospital_service import HospitalService
from translations.languages import t


def show_hospitals():

    # ==========================================
    # CURRENT LANGUAGE
    # ==========================================

    language = st.session_state.get(
        "language",
        "English"
    )

    # ==========================================
    # CHECK LOGIN
    # ==========================================

    Permissions.require_login()

    # ==========================================
    # CURRENT USER
    # ==========================================

    user = SessionManager.get_user()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title(
        f"🏥 {t('hospital_management', language)}"
    )

    # ==========================================
    # ADMIN-ONLY MANAGEMENT SECTION
    # ==========================================

    if Permissions.is_admin():

        st.subheader(
            f"➕ {t('add_hospital', language)}"
        )

        (
            hospital_name,
            address,
            city,
            state,
            pincode,
            contact_number,
            email,
            latitude,
            longitude,
            available_beds,
            available_doctors,
            submitted
        ) = HospitalForm.render()

        # ==========================================
        # ADD HOSPITAL
        # ==========================================

        if submitted:

            db = SessionLocal()

            try:

                success, message = HospitalService.add_hospital(
                    db=db,
                    hospital_name=hospital_name,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    contact_number=contact_number,
                    email=email,
                    latitude=latitude,
                    longitude=longitude,
                    available_beds=available_beds,
                    available_doctors=available_doctors
                )

                if success:

                    st.success(message)
                    st.rerun()

                else:

                    st.error(message)

            finally:

                db.close()

    else:

        st.info(
            f"👤 {t('user_hospital_info', language)}"
        )

    # ==========================================
    # REGISTERED HOSPITALS
    # ==========================================

    st.divider()

    st.subheader(
        f"📋 {t('registered_hospitals', language)}"
    )

    search = st.text_input(
        f"🔍 {t('search_hospital', language)}",
        placeholder=t(
            "search_hospital_placeholder",
            language
        )
    )

    db = SessionLocal()

    try:

        if search.strip():

            hospitals = HospitalService.search_hospitals(
                db,
                search
            )

        else:

            hospitals = HospitalService.get_all_hospitals(
                db
            )

        HospitalTable.render(
            db,
            hospitals
        )

    finally:

        db.close()