import streamlit as st

from translations.languages import t


class InventoryForm:

    @staticmethod
    def render(hospitals, medicines):

        language = st.session_state.get(
            "language",
            "English"
        )

        with st.form(
            "inventory_form",
            clear_on_submit=True
        ):

            st.subheader(
                f"📦 {t('add_inventory', language)}"
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
                f"🏥 {t('hospital', language)}",
                list(hospital_options.keys())
            )

            medicine_name = st.selectbox(
                f"💊 {t('medicine', language)}",
                list(medicine_options.keys())
            )

            col1, col2 = st.columns(2)

            with col1:

                quantity = st.number_input(
                    t("quantity", language),
                    min_value=0,
                    value=0,
                    step=1
                )

            with col2:

                reorder_level = st.number_input(
                    t("reorder_level", language),
                    min_value=0,
                    value=10,
                    step=1
                )

            submitted = st.form_submit_button(
                f"➕ {t('add_inventory', language)}",
                use_container_width=True
            )

        return (
            hospital_options[hospital_name],
            medicine_options[medicine_name],
            quantity,
            reorder_level,
            submitted
        )