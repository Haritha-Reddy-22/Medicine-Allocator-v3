import streamlit as st


class MedicineSearchForm:

    @staticmethod
    def render():

        with st.form("medicine_search_form"):

            medicine_name = st.text_input(
                "💊 Enter Medicine Name",
                placeholder="Example: Paracetamol"
            )

            submitted = st.form_submit_button(
                "🔍 Search Medicine"
            )

        return medicine_name, submitted