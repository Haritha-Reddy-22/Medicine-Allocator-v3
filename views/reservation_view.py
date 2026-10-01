import os

import streamlit as st

from components.forms.reservation_form import ReservationForm
from core.database import SessionLocal
from core.session import SessionManager
from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.reservation_service import ReservationService
from translations.languages import t


def show_prescription(
    prescription_path
):

    if not prescription_path:

        st.warning(
            "Prescription file is not available."
        )

        return

    if not os.path.exists(
        prescription_path
    ):

        st.error(
            "Prescription file could not be found."
        )

        return

    file_extension = os.path.splitext(
        prescription_path
    )[1].lower()

    # ==========================================
    # IMAGE
    # ==========================================

    if file_extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        st.image(
            prescription_path,
            caption="Uploaded Prescription",
            use_container_width=True
        )

    # ==========================================
    # PDF
    # ==========================================

    elif file_extension == ".pdf":

        with open(
            prescription_path,
            "rb"
        ) as file:

            pdf_data = file.read()

        st.download_button(
            label="📄 Open / Download Prescription",
            data=pdf_data,
            file_name=os.path.basename(
                prescription_path
            ),
            mime="application/pdf",
            key=(
                f"download_prescription_"
                f"{os.path.basename(prescription_path)}"
            ),
            use_container_width=True
        )

    else:

        st.warning(
            "Unsupported prescription file."
        )


def show_reservations():

    language = st.session_state.get(
        "language",
        "English"
    )

    # ==========================================
    # USER / ADMIN ACCESS
    # ==========================================

    SessionManager.require_user()

    current_user_id = (
        SessionManager.get_user_id()
    )

    is_admin = (
        SessionManager.is_admin()
    )

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title(
        f"📌 "
        f"{t('medicine_reservations', language)}"
    )

    db = SessionLocal()

    try:

        # ==========================================
        # GET HOSPITALS & MEDICINES
        # ==========================================

        hospitals = (
            HospitalService.get_all_hospitals(
                db
            )
        )

        medicines = (
            MedicineService.get_all_medicines(
                db
            )
        )

        if not hospitals:

            st.warning(
                t(
                    "please_add_hospital_first",
                    language
                )
            )

            return

        if not medicines:

            st.warning(
                t(
                    "please_add_medicine_first",
                    language
                )
            )

            return

        # ==========================================
        # CREATE RESERVATION
        # USER + ADMIN
        # ==========================================

        st.subheader(
            f"➕ "
            f"{t('create_reservation', language)}"
        )

        (
            hospital_id,
            medicine_id,
            quantity,
            submitted
        ) = ReservationForm.render(
            hospitals,
            medicines
        )

        if submitted:

            # --------------------------------------
            # CHECK PRESCRIPTION REQUIREMENT
            # --------------------------------------

            selected_medicine = (
                MedicineService.get_medicine_by_id(
                    db,
                    medicine_id
                )
            )

            if (
                selected_medicine
                and selected_medicine.prescription_required
            ):

                st.warning(
                    "📄 This medicine requires a "
                    "prescription. Please use the "
                    "Medicine Allocator to upload "
                    "your prescription and submit "
                    "the reservation."
                )

            else:

                success, message = (
                    ReservationService
                    .add_reservation(
                        db=db,
                        user_id=current_user_id,
                        hospital_id=hospital_id,
                        medicine_id=medicine_id,
                        quantity=quantity
                    )
                )

                if success:

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    st.error(
                        message
                    )

        st.divider()

        # ==========================================
        # RESERVATION LIST
        # ==========================================

        st.subheader(
            f"📋 "
            f"{t('reservation_list', language)}"
        )

        if is_admin:

            reservations = (
                ReservationService
                .get_all_reservations(
                    db,
                    is_admin=True
                )
            )

        else:

            reservations = (
                ReservationService
                .get_user_reservations(
                    db,
                    current_user_id
                )
            )

        # ==========================================
        # NO RESERVATIONS
        # ==========================================

        if not reservations:

            st.info(
                t(
                    "no_reservations",
                    language
                )
            )

        else:

            # ==========================================
            # DISPLAY RESERVATIONS
            # ==========================================

            for reservation in reservations:

                hospital_name = (
                    reservation.hospital.hospital_name
                    if reservation.hospital
                    else t(
                        "unknown",
                        language
                    )
                )

                medicine_name = (
                    reservation.medicine.medicine_name
                    if reservation.medicine
                    else t(
                        "unknown",
                        language
                    )
                )

                # ======================================
                # RESERVATION CARD
                # ======================================

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"""
### 🏥 {hospital_name}

**💊 {t('medicine', language)}:** {medicine_name}  
**🔢 {t('quantity', language)}:** {reservation.quantity}  
**📅 {t('reserved_at', language)}:** {reservation.reserved_at}  
**📌 {t('status', language)}:** {reservation.status}
"""
                    )

                    # ==================================
                    # PRESCRIPTION INFORMATION
                    # ==================================

                    prescription_status = getattr(
                        reservation,
                        "prescription_status",
                        "Not Required"
                    )

                    if (
                        prescription_status
                        != "Not Required"
                    ):

                        st.markdown(
                            f"📄 **Prescription Status:** "
                            f"{prescription_status}"
                        )

                    # ==================================
                    # ADMIN ACTIONS
                    # ==================================

                    if is_admin:

                        # ==================================
                        # PRESCRIPTION REVIEW
                        # ==================================

                        if (
                            prescription_status
                            == "Pending Review"
                        ):

                            st.divider()

                            st.subheader(
                                "📄 Prescription Review"
                            )

                            show_prescription(
                                reservation.prescription_path
                            )

                            col1, col2 = st.columns(
                                2
                            )

                            # ------------------------------
                            # APPROVE PRESCRIPTION
                            # ------------------------------

                            with col1:

                                if st.button(
                                    "✅ Approve Prescription",
                                    key=(
                                        f"approve_prescription_"
                                        f"{reservation.id}"
                                    ),
                                    use_container_width=True
                                ):

                                    (
                                        success,
                                        message
                                    ) = (
                                        ReservationService
                                        .approve_prescription(
                                            db=db,
                                            reservation_id=(
                                                reservation.id
                                            ),
                                            is_admin=True
                                        )
                                    )

                                    if success:

                                        st.success(
                                            message
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            message
                                        )

                            # ------------------------------
                            # REJECT PRESCRIPTION
                            # ------------------------------

                            with col2:

                                if st.button(
                                    "❌ Reject Prescription",
                                    key=(
                                        f"reject_prescription_"
                                        f"{reservation.id}"
                                    ),
                                    use_container_width=True
                                ):

                                    (
                                        success,
                                        message
                                    ) = (
                                        ReservationService
                                        .reject_prescription(
                                            db=db,
                                            reservation_id=(
                                                reservation.id
                                            ),
                                            is_admin=True
                                        )
                                    )

                                    if success:

                                        st.success(
                                            message
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            message
                                        )

                        # ==================================
                        # NORMAL PENDING RESERVATION
                        # ==================================

                        if reservation.status == "Pending":

                            # ----------------------------------
                            # APPROVE
                            # ----------------------------------

                            col1, col2 = st.columns(
                                2
                            )

                            with col1:

                                if st.button(
                                    f"✅ "
                                    f"{t('approve', language)}",
                                    key=(
                                        f"approve_"
                                        f"{reservation.id}"
                                    ),
                                    use_container_width=True
                                ):

                                    (
                                        success,
                                        message
                                    ) = (
                                        ReservationService
                                        .approve_reservation(
                                            db=db,
                                            reservation_id=(
                                                reservation.id
                                            ),
                                            is_admin=True
                                        )
                                    )

                                    if success:

                                        st.success(
                                            message
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            message
                                        )

                            # ----------------------------------
                            # REJECT / CANCEL
                            # ----------------------------------

                            with col2:

                                if st.button(
                                    f"❌ "
                                    f"{t('reject', language)}",
                                    key=(
                                        f"reject_"
                                        f"{reservation.id}"
                                    ),
                                    use_container_width=True
                                ):

                                    (
                                        success,
                                        message
                                    ) = (
                                        ReservationService
                                        .cancel_reservation(
                                            db=db,
                                            reservation_id=(
                                                reservation.id
                                            ),
                                            current_user_id=(
                                                current_user_id
                                            ),
                                            is_admin=True
                                        )
                                    )

                                    if success:

                                        st.success(
                                            message
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            message
                                        )

                        # ==================================
                        # APPROVED → COMPLETE
                        # ==================================

                        elif reservation.status == "Approved":

                            if st.button(
                                f"🏁 "
                                f"{t('mark_completed', language)}",
                                key=(
                                    f"complete_"
                                    f"{reservation.id}"
                                ),
                                use_container_width=True
                            ):

                                (
                                    success,
                                    message
                                ) = (
                                    ReservationService
                                    .complete_reservation(
                                        db=db,
                                        reservation_id=(
                                            reservation.id
                                        ),
                                        is_admin=True
                                    )
                                )

                                if success:

                                    st.success(
                                        message
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        message
                                    )

                    # ======================================
                    # USER ACTIONS
                    # ======================================

                    else:

                        if reservation.status in [
                            "Pending",
                            "Pending Review"
                        ]:

                            if st.button(
                                f"❌ "
                                f"{t('cancel_reservation', language)}",
                                key=(
                                    f"user_cancel_"
                                    f"{reservation.id}"
                                ),
                                use_container_width=True
                            ):

                                (
                                    success,
                                    message
                                ) = (
                                    ReservationService
                                    .cancel_reservation(
                                        db=db,
                                        reservation_id=(
                                            reservation.id
                                        ),
                                        current_user_id=(
                                            current_user_id
                                        ),
                                        is_admin=False
                                    )
                                )

                                if success:

                                    st.success(
                                        message
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        message
                                    )

                st.divider()

    finally:

        db.close()