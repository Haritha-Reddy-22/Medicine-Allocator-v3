import streamlit as st
from datetime import date


class MedicineForm:

    @staticmethod
    def render():

        with st.form("medicine_form", clear_on_submit=True):

            st.subheader("💊 Add Medicine")

            medicine_name = st.text_input(
                "Medicine Name"
            )

            generic_name = st.text_input(
                "Generic Name"
            )

            category = st.selectbox(
                "Category",
                [
                    "Tablet",
                    "Capsule",
                    "Syrup",
                    "Injection",
                    "Cream",
                    "Ointment",
                    "Drops",
                    "Inhaler",
                    "Other"
                ]
            )

            manufacturer = st.text_input(
                "Manufacturer"
            )

            batch_number = st.text_input(
                "Batch Number"
            )

            expiry_date = st.date_input(
                "Expiry Date",
                min_value=date.today()
            )

            unit_price = st.number_input(
                "Unit Price (₹)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                format="%.2f"
            )

            description = st.text_area(
                "Description"
            )

            submitted = st.form_submit_button(
                "➕ Add Medicine",
                use_container_width=True
            )

        return (
            medicine_name,
            generic_name,
            category,
            manufacturer,
            batch_number,
            expiry_date,
            unit_price,
            description,
            submitted
        )