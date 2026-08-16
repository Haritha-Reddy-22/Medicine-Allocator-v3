import streamlit as st

from components.forms.reservation_form import ReservationForm
from core.database import SessionLocal
from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.reservation_service import ReservationService


def show_reservations():

    st.title("📌 Medicine Reservations")

    db = SessionLocal()

    try:

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)

        if not hospitals:
            st.warning("Please add at least one hospital first.")
            return

        if not medicines:
            st.warning("Please add at least one medicine first.")
            return

        # --------------------------------------------------
        # CREATE RESERVATION
        # --------------------------------------------------

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

            success, message = ReservationService.add_reservation(
                db=db,
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                quantity=quantity
            )

            if success:
                st.success(message)
                st.rerun()

            else:
                st.error(message)

        st.divider()

        # --------------------------------------------------
        # RESERVATION LIST
        # --------------------------------------------------

        st.subheader("📋 Reservation List")

        reservations = ReservationService.get_all_reservations(db)

        if not reservations:

            st.info("No reservations available.")

        else:

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

                # --------------------------------------------------
                # PENDING ACTIONS
                # --------------------------------------------------

                if reservation.status == "Pending":

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "✅ Approve",
                            key=f"approve_{reservation.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                ReservationService.approve_reservation(
                                    db=db,
                                    reservation_id=reservation.id
                                )
                            )

                            if success:
                                st.success(message)
                                st.rerun()

                            else:
                                st.error(message)

                    with col2:

                        if st.button(
                            "❌ Reject",
                            key=f"reject_{reservation.id}",
                            use_container_width=True
                        ):

                            success, message = (
                                ReservationService.cancel_reservation(
                                    db=db,
                                    reservation_id=reservation.id
                                )
                            )

                            if success:
                                st.success(message)
                                st.rerun()

                            else:
                                st.error(message)

                # --------------------------------------------------
                # APPROVED ACTION
                # --------------------------------------------------

                elif reservation.status == "Approved":

                    if st.button(
                        "🏁 Mark as Completed",
                        key=f"complete_{reservation.id}",
                        use_container_width=True
                    ):

                        success, message = (
                            ReservationService.complete_reservation(
                                db=db,
                                reservation_id=reservation.id
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