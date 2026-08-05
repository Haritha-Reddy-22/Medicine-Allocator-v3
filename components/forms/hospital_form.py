import streamlit as st


class HospitalForm:

    @staticmethod
    def render():

        with st.form("hospital_form", clear_on_submit=True):

            st.subheader("🏥 Add Hospital")

            hospital_name = st.text_input("Hospital Name")

            address = st.text_area("Address")

            col1, col2 = st.columns(2)

            with col1:
                city = st.text_input("City")

            with col2:
                state = st.text_input("State")

            col3, col4 = st.columns(2)

            with col3:
                pincode = st.text_input("Pincode")

            with col4:
                contact_number = st.text_input("Contact Number")

            email = st.text_input("Email")

            col5, col6 = st.columns(2)

            with col5:
                latitude = st.number_input(
                    "Latitude",
                    value=0.0,
                    format="%.6f"
                )

            with col6:
                longitude = st.number_input(
                    "Longitude",
                    value=0.0,
                    format="%.6f"
                )

            col7, col8 = st.columns(2)

            with col7:
                available_beds = st.number_input(
                    "Available Beds",
                    min_value=0,
                    value=0,
                    step=1
                )

            with col8:
                available_doctors = st.number_input(
                    "Available Doctors",
                    min_value=0,
                    value=0,
                    step=1
                )

            submitted = st.form_submit_button(
                "➕ Add Hospital",
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