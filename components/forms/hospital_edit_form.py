import streamlit as st


class HospitalEditForm:

    @staticmethod
    def render(hospital):

        with st.form(f"edit_form_{hospital.id}"):

            st.subheader("✏️ Edit Hospital")

            hospital_name = st.text_input(
                "Hospital Name",
                value=hospital.hospital_name
            )

            city = st.text_input(
                "City",
                value=hospital.city
            )

            state = st.text_input(
                "State",
                value=hospital.state
            )

            available_beds = st.number_input(
                "Available Beds",
                min_value=0,
                value=hospital.available_beds,
                step=1
            )

            available_doctors = st.number_input(
                "Available Doctors",
                min_value=0,
                value=hospital.available_doctors,
                step=1
            )

            save = st.form_submit_button(
                "💾 Save Changes",
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