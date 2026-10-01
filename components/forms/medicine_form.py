
import streamlit as st
from datetime import date

from translations.languages import t


class MedicineForm:

    @staticmethod
    def render():

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form(
            "medicine_form",
            clear_on_submit=True
        ):

            st.subheader(
                f"💊 {t('add_medicine', language)}"
            )

            medicine_name = st.text_input(
                t("medicine_name", language)
            )

            generic_name = st.text_input(
                t("generic_name", language)
            )

            category = st.selectbox(
                t("category", language),
                [
                    t("tablet", language),
                    t("capsule", language),
                    t("syrup", language),
                    t("injection", language),
                    t("cream", language),
                    t("ointment", language),
                    t("drops", language),
                    t("inhaler", language),
                    t("other", language)
                ]
            )

            manufacturer = st.text_input(
                t("manufacturer", language)
            )

            batch_number = st.text_input(
                t("batch_number", language)
            )

            expiry_date = st.date_input(
                t("expiry_date", language),
                min_value=date.today()
            )

            unit_price = st.number_input(
                t("unit_price", language),
                min_value=0.0,
                value=0.0,
                step=1.0,
                format="%.2f"
            )

            description = st.text_area(
                t("description", language)
            )

            # ======================================
            # PRESCRIPTION REQUIREMENT
            # ======================================

            prescription_required = st.selectbox(
                "📄 Prescription Required?",
                ["No", "Yes"],
                index=0
            )

            prescription_required = (
                prescription_required == "Yes"
            )

            submitted = st.form_submit_button(
                f"➕ {t('add_medicine', language)}",
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
            prescription_required,
            submitted
        )

