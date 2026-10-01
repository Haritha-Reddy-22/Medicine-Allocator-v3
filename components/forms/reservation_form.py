import streamlit as st

from translations.languages import t


class ReservationForm:

    @staticmethod
    def render(hospitals, medicines):

        language = st.session_state.get(
            "language",
            "English"
        )

        hospital_options = {
            hospital.hospital_name: hospital.id
            for hospital in hospitals
        }

        medicine_options = {
            medicine.medicine_name: medicine.id
            for medicine in medicines
        }

        hospital_name = st.selectbox(
            f"🏥 {t('select_hospital', language)}",
            list(hospital_options.keys())
        )

        medicine_name = st.selectbox(
            f"💊 {t('select_medicine', language)}",
            list(medicine_options.keys())
        )

        quantity = st.number_input(
            t("quantity", language),
            min_value=1,
            value=1,
            step=1
        )

        submitted = st.button(
            f"📌 {t('create_reservation', language)}",
            use_container_width=True
        )

        return (
            hospital_options[hospital_name],
            medicine_options[medicine_name],
            quantity,
            submitted
        )