import streamlit as st

from components.forms.hospital_form import HospitalForm
from components.tables.hospital_table import HospitalTable
from core.database import SessionLocal
from services.hospital_service import HospitalService


def show_hospitals():

    st.title("🏥 Hospital Management")

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

    st.divider()

    st.subheader("📋 Registered Hospitals")

    search = st.text_input(
        "🔍 Search Hospital",
        placeholder="Search by Hospital Name, City or State"
    )

    db = SessionLocal()

    try:

        if search.strip():

            hospitals = HospitalService.search_hospitals(
                db,
                search
            )

        else:

            hospitals = HospitalService.get_all_hospitals(db)

        HospitalTable.render(
            db,
            hospitals
        )

    finally:

        db.close()