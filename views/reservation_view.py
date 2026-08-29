
import streamlit as st

from components.forms.reservation_form import ReservationForm
from core.database import SessionLocal
from core.session import SessionManager
from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.reservation_service import ReservationService


def show_reservations():

    # ==========================================
    # USER / ADMIN ACCESS
    # ==========================================

    SessionManager.require_user()

    current_user_id = SessionManager.get_user_id()
    is_admin = SessionManager.is_admin()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title("📌 Medicine Reservations")

    db = SessionLocal()

    try:

        # ==========================================
        # GET HOSPITALS & MEDICINES
        # ==========================================

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)

        if not hospitals:

            st.warning(
                "Please add at least one hospital first."
            )

            return

        if not medicines:

            st.warning(
                "Please add at least one medicine first."
            )

            return

        # ==========================================
        # CREATE RESERVATION
        # USER + ADMIN
        # ==========================================

        st.subheader("➕ Create Reservation")

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

            success, message = (
                ReservationService.add_reservation(
                    db=db,
                    user_id=current_user_id,
                    hospital_id=hospital_id,
                    medicine_id=medicine_id,
                    quantity=quantity
                )
            )

            if success:

                st.success(message)
                st.rerun()

            else:

                st.error(message)

        st.divider()

        # ==========================================
        # RESERVATION LIST
        # ==========================================

        st.subheader("📋 Reservation List")

        if is_admin:

            # --------------------------------------
            # ADMIN → ALL RESERVATIONS
            # --------------------------------------

            reservations = (
                ReservationService.get_all_reservations(
                    db,
                    is_admin=True
                )
            )

        else:

            # --------------------------------------
            # USER → ONLY THEIR RESERVATIONS
            # --------------------------------------

            reservations = (
                ReservationService.get_user_reservations(
                    db,
                    current_user_id
                )
            )

        # ==========================================
        # NO RESERVATIONS
        # ==========================================

        if not reservations:

            st.info(
                "No reservations available."
            )

        else:

            # ==========================================
            # DISPLAY RESERVATIONS
            # ==========================================

            for reservation in reservations:

                hospital_name = (
                    reservation.hospital.hospital_name
                    if reservation.hospital
                    else "Unknown"
                )

                medicine_name = (
                    reservation.medicine.medicine_name
                    if reservation.medicine
                    else "Unknown"
                )

                st.markdown(
                    f"""
### 🏥 {hospital_name}

**💊 Medicine:** {medicine_name}  
**🔢 Quantity:** {reservation.quantity}  
**📅 Reserved At:** {reservation.reserved_at}  
**📌 Status:** {reservation.status}
"""
                )

                # ==========================================
                # ADMIN ACTIONS
                # ==========================================

                if is_admin:

                    # ======================================
                    # PENDING → APPROVE / REJECT
                    # ======================================

                    if reservation.status == "Pending":

                        col1, col2 = st.columns(2)

                        # ----------------------------------
                        # APPROVE
                        # ----------------------------------

                        with col1:

                            if st.button(
                                "✅ Approve",
                                key=f"approve_{reservation.id}",
                                use_container_width=True
                            ):

                                success, message = (
                                    ReservationService
                                    .approve_reservation(
                                        db=db,
                                        reservation_id=reservation.id,
                                        is_admin=True
                                    )
                                )

                                if success:

                                    st.success(message)
                                    st.rerun()

                                else:

                                    st.error(message)

                        # ----------------------------------
                        # REJECT
                        # ----------------------------------

                        with col2:

                            if st.button(
                                "❌ Reject",
                                key=f"reject_{reservation.id}",
                                use_container_width=True
                            ):

                                success, message = (
                                    ReservationService
                                    .cancel_reservation(
                                        db=db,
                                        reservation_id=reservation.id,
                                        current_user_id=current_user_id,
                                        is_admin=True
                                    )
                                )

                                if success:

                                    st.success(message)
                                    st.rerun()

                                else:

                                    st.error(message)

                    # ======================================
                    # APPROVED → COMPLETE
                    # ======================================

                    elif reservation.status == "Approved":

                        if st.button(
                            "🏁 Mark as Completed",
                            key=f"complete_{reservation.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                ReservationService
                                .complete_reservation(
                                    db=db,
                                    reservation_id=reservation.id,
                                    is_admin=True
                                )
                            )

                            if success:

                                st.success(message)
                                st.rerun()

                            else:

                                st.error(message)

                # ==========================================
                # USER ACTIONS
                # ==========================================

                else:

                    # --------------------------------------
                    # USER CAN CANCEL OWN PENDING RESERVATION
                    # --------------------------------------

                    if reservation.status == "Pending":

                        if st.button(
                            "❌ Cancel Reservation",
                            key=f"user_cancel_{reservation.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                ReservationService
                                .cancel_reservation(
                                    db=db,
                                    reservation_id=reservation.id,
                                    current_user_id=current_user_id,
                                    is_admin=False
                                )
                            )

                            if success:

                                st.success(message)
                                st.rerun()

                            else:

                                st.error(message)

                st.divider()

    finally:

        db.close()
