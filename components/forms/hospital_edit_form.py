import streamlit as st

from translations.languages import t


class HospitalEditForm:

    @staticmethod
    def render(hospital):

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form(
            f"edit_form_{hospital.id}"
        ):

            st.subheader(
                f"✏️ {t('edit_hospital', language)}"
            )

            hospital_name = st.text_input(
                t("hospital_name", language),
                value=hospital.hospital_name
            )

            city = st.text_input(
                t("city", language),
                value=hospital.city
            )

            state = st.text_input(
                t("state", language),
                value=hospital.state
            )

            available_beds = st.number_input(
                t("available_beds", language),
                min_value=0,
                value=hospital.available_beds,
                step=1
            )

            available_doctors = st.number_input(
                t("available_doctors", language),
                min_value=0,
                value=hospital.available_doctors,
                step=1
            )

            save = st.form_submit_button(
                f"💾 {t('save_changes', language)}",
                use_container_width=True
            )

        return (
            hospital_name,
            city,
            state,
            available_beds,
            available_doctors,
            save
        )