import streamlit as st


class ReservationForm:

    @staticmethod
    def render(hospitals, medicines):

        hospital_options = {
            hospital.hospital_name: hospital.id
            for hospital in hospitals
        }

        medicine_options = {
            medicine.medicine_name: medicine.id
            for medicine in medicines
        }

        hospital_name = st.selectbox(
            "Select Hospital",
            list(hospital_options.keys())
        )

        medicine_name = st.selectbox(
            "Select Medicine",
            list(medicine_options.keys())
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1
        )

        submitted = st.button(
            "📌 Create Reservation",
            use_container_width=True
        )

        return (
            hospital_options[hospital_name],
            medicine_options[medicine_name],
            quantity,
            submitted
        )