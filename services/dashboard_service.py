from sqlalchemy.orm import Session

from models.hospital import Hospital
from models.inventory import Inventory
from models.medicine import Medicine


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

        return {
            "hospitals": hospitals,
            "medicines": medicines,
            "inventory": inventory,
            "low_stock": low_stock
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