import streamlit as st

from translations.languages import t


class HospitalForm:

    @staticmethod
    def render():

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form(
            "hospital_form",
            clear_on_submit=True
        ):

            st.subheader(
                f"🏥 {t('add_hospital', language)}"
            )

            hospital_name = st.text_input(
                t("hospital_name", language)
            )

            address = st.text_area(
                t("address", language)
            )

            col1, col2 = st.columns(2)

            with col1:

                city = st.text_input(
                    t("city", language)
                )

            with col2:

                state = st.text_input(
                    t("state", language)
                )

            col3, col4 = st.columns(2)

            with col3:

                pincode = st.text_input(
                    t("pincode", language)
                )

            with col4:

                contact_number = st.text_input(
                    t("contact_number", language)
                )

            email = st.text_input(
                t("email", language)
            )

            col5, col6 = st.columns(2)

            with col5:

                latitude = st.number_input(
                    t("latitude", language),
                    value=0.0,
                    format="%.6f"
                )

            with col6:

                longitude = st.number_input(
                    t("longitude", language),
                    value=0.0,
                    format="%.6f"
                )

            col7, col8 = st.columns(2)

            with col7:

                available_beds = st.number_input(
                    t("available_beds", language),
                    min_value=0,
                    value=0,
                    step=1
                )

            with col8:

                available_doctors = st.number_input(
                    t("available_doctors", language),
                    min_value=0,
                    value=0,
                    step=1
                )

            submitted = st.form_submit_button(
                f"➕ {t('add_hospital', language)}",
                use_container_width=True
            )

        return (
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
        )