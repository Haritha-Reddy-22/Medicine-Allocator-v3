import streamlit as st

from components.forms.medicine_form import MedicineForm
from components.tables.medicine_table import MedicineTable
from core.database import SessionLocal
from services.medicine_service import MedicineService


def show_medicines():

    st.title("💊 Medicine Management")

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

    st.subheader("📋 Registered Medicines")

    search = st.text_input(
        "🔍 Search Medicine"
    )

    db = SessionLocal()

    try:

        if search.strip():

            medicines = MedicineService.search_medicines(
                db,
                search
            )

        else:

            medicines = MedicineService.get_all_medicines(db)

        MedicineTable.render(
            db,
            medicines
        )

    finally:

        db.close()