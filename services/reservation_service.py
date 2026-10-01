from models.inventory import Inventory
from models.reservation import Reservation
from models.medicine import Medicine


class ReservationService:

    # ==========================================
    # CREATE RESERVATION
    # USER + ADMIN
    # ==========================================

    @staticmethod
    def add_reservation(
        db,
        user_id,
        hospital_id,
        medicine_id,
        quantity,
        prescription_path=None
    ):

        try:

            if not user_id:
                return False, "User information is required."

            if quantity <= 0:
                return (
                    False,
                    "Reservation quantity must be greater than zero."
                )

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.hospital_id == hospital_id,
                    Inventory.medicine_id == medicine_id
                )
                .first()
            )

            if not inventory:

                return (
                    False,
                    "Medicine is not available in this hospital."
                )

            if inventory.quantity < quantity:

                return (
                    False,
                    "Insufficient stock available."
                )

            medicine = (
                db.query(Medicine)
                .filter(
                    Medicine.id == medicine_id
                )
                .first()
            )

            if not medicine:

                return (
                    False,
                    "Medicine not found."
                )

            # ======================================
            # PRESCRIPTION VALIDATION
            # ======================================

            if medicine.prescription_required:

                if not prescription_path:

                    return (
                        False,
                        "A prescription is required for this medicine."
                    )

                reservation_status = "Pending Review"
                prescription_status = "Pending Review"

            else:

                reservation_status = "Pending"
                prescription_status = "Not Required"

            # ======================================
            # CREATE RESERVATION
            # ======================================

            reservation = Reservation(
                user_id=user_id,
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                quantity=quantity,
                status=reservation_status,
                prescription_path=prescription_path,
                prescription_status=prescription_status
            )

            db.add(reservation)
            db.commit()
            db.refresh(reservation)

            if medicine.prescription_required:

                return (
                    True,
                    "Prescription submitted successfully. "
                    "Your reservation is pending review."
                )

            return (
                True,
                "Reservation request created successfully."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)

    # ==========================================
    # GET ALL RESERVATIONS
    # ADMIN ONLY
    # ==========================================

    @staticmethod
    def get_all_reservations(
        db,
        is_admin=False
    ):

        if not is_admin:
            return []

        return (
            db.query(Reservation)
            .order_by(
                Reservation.reserved_at.desc()
            )
            .all()
        )

    # ==========================================
    # GET USER RESERVATIONS
    # ==========================================

    @staticmethod
    def get_user_reservations(
        db,
        user_id
    ):

        if not user_id:
            return []

        return (
            db.query(Reservation)
            .filter(
                Reservation.user_id == user_id
            )
            .order_by(
                Reservation.reserved_at.desc()
            )
            .all()
        )

    # ==========================================
    # APPROVE RESERVATION
    # ADMIN ONLY
    # ==========================================

    @staticmethod
    def approve_reservation(
        db,
        reservation_id,
        is_admin=False
    ):

        try:

            if not is_admin:

                return (
                    False,
                    "Administrator privileges are required."
                )

            reservation = (
                db.query(Reservation)
                .filter(
                    Reservation.id == reservation_id
                )
                .first()
            )

            if not reservation:

                return (
                    False,
                    "Reservation not found."
                )

            # ======================================
            # NORMAL RESERVATION
            # OR PRESCRIPTION APPROVED
            # ======================================

            allowed_statuses = [
                "Pending",
                "Pending Review"
            ]

            if reservation.status not in allowed_statuses:

                return (
                    False,
                    "Only pending reservations can be approved."
                )

            # ======================================
            # PRESCRIPTION CHECK
            # ======================================

            if (
                reservation.prescription_status
                == "Pending Review"
            ):

                return (
                    False,
                    "Prescription review is required before "
                    "this reservation can be approved."
                )

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.hospital_id
                    == reservation.hospital_id,

                    Inventory.medicine_id
                    == reservation.medicine_id
                )
                .first()
            )

            if not inventory:

                return (
                    False,
                    "Medicine inventory not found."
                )

            if inventory.quantity < reservation.quantity:

                return (
                    False,
                    "Insufficient stock available."
                )

            inventory.quantity -= reservation.quantity

            reservation.status = "Approved"

            db.commit()
            db.refresh(reservation)

            return (
                True,
                "Reservation approved successfully."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)

    # ==========================================
    # APPROVE PRESCRIPTION
    # ADMIN ONLY
    # ==========================================

    @staticmethod
    def approve_prescription(
        db,
        reservation_id,
        is_admin=False
    ):

        try:

            if not is_admin:

                return (
                    False,
                    "Administrator privileges are required."
                )

            reservation = (
                db.query(Reservation)
                .filter(
                    Reservation.id == reservation_id
                )
                .first()
            )

            if not reservation:

                return (
                    False,
                    "Reservation not found."
                )

            if reservation.prescription_status != "Pending Review":

                return (
                    False,
                    "This prescription is not pending review."
                )

            reservation.prescription_status = "Approved"

            # The reservation itself remains pending
            # until the admin approves the reservation.

            reservation.status = "Pending"

            db.commit()
            db.refresh(reservation)

            return (
                True,
                "Prescription approved successfully. "
                "Reservation can now be approved."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)

    # ==========================================
    # REJECT PRESCRIPTION
    # ADMIN ONLY
    # ==========================================

    @staticmethod
    def reject_prescription(
        db,
        reservation_id,
        is_admin=False
    ):

        try:

            if not is_admin:

                return (
                    False,
                    "Administrator privileges are required."
                )

            reservation = (
                db.query(Reservation)
                .filter(
                    Reservation.id == reservation_id
                )
                .first()
            )

            if not reservation:

                return (
                    False,
                    "Reservation not found."
                )

            if reservation.prescription_status != "Pending Review":

                return (
                    False,
                    "This prescription is not pending review."
                )

            reservation.prescription_status = "Rejected"
            reservation.status = "Rejected"

            db.commit()
            db.refresh(reservation)

            return (
                True,
                "Prescription rejected."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)

    # ==========================================
    # CANCEL RESERVATION
    # ==========================================

    @staticmethod
    def cancel_reservation(
        db,
        reservation_id,
        current_user_id=None,
        is_admin=False
    ):

        try:

            reservation = (
                db.query(Reservation)
                .filter(
                    Reservation.id == reservation_id
                )
                .first()
            )

            if not reservation:

                return (
                    False,
                    "Reservation not found."
                )

            if reservation.status not in [
                "Pending",
                "Pending Review"
            ]:

                return (
                    False,
                    "Only pending reservations can be cancelled."
                )

            # ======================================
            # ADMIN
            # ======================================

            if is_admin:

                reservation.status = "Cancelled"

            # ======================================
            # USER
            # ======================================

            else:

                if not current_user_id:

                    return (
                        False,
                        "User information is required."
                    )

                if reservation.user_id != current_user_id:

                    return (
                        False,
                        "You can only cancel your own reservation."
                    )

                reservation.status = "Cancelled"

            db.commit()
            db.refresh(reservation)

            return (
                True,
                "Reservation cancelled successfully."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)

    # ==========================================
    # COMPLETE RESERVATION
    # ADMIN ONLY
    # ==========================================

    @staticmethod
    def complete_reservation(
        db,
        reservation_id,
        is_admin=False
    ):

        try:

            if not is_admin:

                return (
                    False,
                    "Administrator privileges are required."
                )

            reservation = (
                db.query(Reservation)
                .filter(
                    Reservation.id == reservation_id
                )
                .first()
            )

            if not reservation:

                return (
                    False,
                    "Reservation not found."
                )

            if reservation.status != "Approved":

                return (
                    False,
                    "Only approved reservations can be completed."
                )

            reservation.status = "Completed"

            db.commit()
            db.refresh(reservation)

            return (
                True,
                "Reservation completed successfully."
            )

        except Exception as e:

            db.rollback()

            return False, str(e)