from sqlalchemy.orm import Session

from models.hospital import Hospital
from models.inventory import Inventory
from models.medicine import Medicine
from models.reservation import Reservation


class DashboardService:

    @staticmethod
    def get_statistics(db: Session):

        hospitals = db.query(Hospital).count()

        medicines = db.query(Medicine).count()

        inventory = db.query(Inventory).count()

        low_stock = (
            db.query(Inventory)
            .filter(
                Inventory.quantity <= Inventory.reorder_level
            )
            .count()
        )

        reservations = db.query(Reservation).count()

        pending_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.status == "Pending"
            )
            .count()
        )

        approved_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.status == "Approved"
            )
            .count()
        )

        completed_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.status == "Completed"
            )
            .count()
        )

        cancelled_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.status == "Cancelled"
            )
            .count()
        )

        return {
            "hospitals": hospitals,
            "medicines": medicines,
            "inventory": inventory,
            "low_stock": low_stock,

            "reservations": reservations,

            "pending_reservations":
                pending_reservations,

            "approved_reservations":
                approved_reservations,

            "completed_reservations":
                completed_reservations,

            "cancelled_reservations":
                cancelled_reservations
        }

    @staticmethod
    def get_low_stock(db: Session):

        return (
            db.query(Inventory)
            .filter(
                Inventory.quantity <= Inventory.reorder_level
            )
            .all()
        )

    @staticmethod
    def get_reservations(db: Session):

        return (
            db.query(Reservation)
            .order_by(
                Reservation.reserved_at.desc()
            )
            .all()
        )