import streamlit as st

from components.forms.hospital_edit_form import HospitalEditForm
from services.hospital_service import HospitalService
from utils.permissions import Permissions


class HospitalTable:

    @staticmethod
    def render(db, hospitals):

        if not hospitals:

            st.info("No hospitals found.")
            return

        is_admin = Permissions.is_admin()

        for hospital in hospitals:

            # ==========================================
            # USER VIEW
            # ==========================================

            if not is_admin:

                with st.container(border=True):

                    st.markdown(
                        f"""
### 🏥 {hospital.hospital_name}

📍 {hospital.city}, {hospital.state}

🛏 Beds : {hospital.available_beds}

👨‍⚕️ Doctors : {hospital.available_doctors}
"""
                    )

            # ==========================================
            # ADMIN VIEW
            # ==========================================

            else:

                with st.container(border=True):

                    col1, col2, col3 = st.columns([6, 2, 2])

                    with col1:

                        st.markdown(
                            f"""
### 🏥 {hospital.hospital_name}

📍 {hospital.city}, {hospital.state}

🛏 Beds : {hospital.available_beds}

👨‍⚕️ Doctors : {hospital.available_doctors}
"""
                        )

                    # ----------------------------------
                    # EDIT
                    # ----------------------------------

                    with col2:

                        if st.button(
                            "✏️ Edit",
                            key=f"edit_{hospital.id}"
                        ):

                            st.session_state["edit_hospital"] = hospital.id

                    # ----------------------------------
                    # DELETE
                    # ----------------------------------

                    with col3:

                        if st.button(
                            "🗑 Delete",
                            key=f"delete_{hospital.id}"
                        ):

                            success, message = (
                                HospitalService.delete_hospital(
                                    db,
                                    hospital.id
                                )
                            )

                            if success:

                                st.success(message)

                                st.rerun()

                            else:

                                st.error(message)

                    # ----------------------------------
                    # EDIT FORM
                    # ----------------------------------

                    if (
                        st.session_state.get("edit_hospital")
                        == hospital.id
                    ):

                        (
                            hospital_name,
                            city,
                            state,
                            available_beds,
                            available_doctors,
                            save
                        ) = HospitalEditForm.render(hospital)

                        if save:

                            success, message = (
                                HospitalService.update_hospital(
                                    db=db,
                                    hospital_id=hospital.id,
                                    hospital_name=hospital_name,
                                    city=city,
                                    state=state,
                                    available_beds=available_beds,
                                    available_doctors=available_doctors
                                )
                            )

                            if success:

                                st.success(message)

                                st.session_state.pop(
                                    "edit_hospital",
                                    None
                                )

                                st.rerun()

                            else:

                                st.error(message)