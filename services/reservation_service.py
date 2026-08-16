from models.inventory import Inventory
from models.reservation import Reservation


class ReservationService:

    @staticmethod
    def add_reservation(
        db,
        hospital_id,
        medicine_id,
        quantity
    ):

        try:

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.hospital_id == hospital_id,
                    Inventory.medicine_id == medicine_id
                )
                .first()
            )

            if not inventory:
                return False, "Medicine is not available in this hospital."

            if inventory.quantity < quantity:
                return False, "Insufficient stock available."

            reservation = Reservation(
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                quantity=quantity,
                status="Pending"
            )

            db.add(reservation)
            db.commit()
            db.refresh(reservation)

            return True, "Reservation request created successfully."

        except Exception as e:

            db.rollback()

            return False, str(e)

    @staticmethod
    def get_all_reservations(db):

        return (
            db.query(Reservation)
            .order_by(Reservation.reserved_at.desc())
            .all()
        )

    @staticmethod
    def approve_reservation(
        db,
        reservation_id
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
                return False, "Reservation not found."

            if reservation.status != "Pending":
                return False, "Only pending reservations can be approved."

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.hospital_id == reservation.hospital_id,
                    Inventory.medicine_id == reservation.medicine_id
                )
                .first()
            )

            if not inventory:
                return False, "Medicine inventory not found."

            if inventory.quantity < reservation.quantity:
                return False, "Insufficient stock available."

            inventory.quantity -= reservation.quantity

            reservation.status = "Approved"

            db.commit()
            db.refresh(reservation)

            return True, "Reservation approved successfully."

        except Exception as e:

            db.rollback()

            return False, str(e)

    @staticmethod
    def cancel_reservation(
        db,
        reservation_id
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
                return False, "Reservation not found."

            if reservation.status != "Pending":
                return False, "Only pending reservations can be cancelled."

            reservation.status = "Cancelled"

            db.commit()
            db.refresh(reservation)

            return True, "Reservation cancelled successfully."

        except Exception as e:

            db.rollback()

            return False, str(e)

    @staticmethod
    def complete_reservation(
        db,
        reservation_id
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
                return False, "Reservation not found."

            if reservation.status != "Approved":
                return False, "Only approved reservations can be completed."

            reservation.status = "Completed"

            db.commit()
            db.refresh(reservation)

            return True, "Reservation completed successfully."

        except Exception as e:

            db.rollback()

            return False, str(e)